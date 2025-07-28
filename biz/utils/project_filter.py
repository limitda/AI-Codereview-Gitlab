import os
import fnmatch
from typing import List
from biz.utils.log import logger


class ProjectFilter:
    """项目过滤器，用于判断项目是否需要进行代码审查"""

    def __init__(self):
        self.excluded_projects = self._get_excluded_projects()
        self.included_projects = self._get_included_projects()

    def _get_excluded_projects(self) -> List[str]:
        """获取排除的项目列表"""
        excluded = os.environ.get('EXCLUDED_PROJECTS', '')
        if excluded:
            return [project.strip() for project in excluded.split(',') if project.strip()]
        return []

    def _get_included_projects(self) -> List[str]:
        """获取包含的项目列表"""
        included = os.environ.get('INCLUDED_PROJECTS', '')
        if included:
            return [project.strip() for project in included.split(',') if project.strip()]
        return []

    def _matches_pattern(self, project_name: str, patterns: List[str]) -> bool:
        """
        检查项目名称是否匹配任一模式
        支持通配符: * 匹配任意字符, ? 匹配单个字符
        :param project_name: 项目名称
        :param patterns: 模式列表
        :return: True表示匹配，False表示不匹配
        """
        for pattern in patterns:
            if fnmatch.fnmatch(project_name, pattern):
                logger.debug(f"项目 {project_name} 匹配模式 {pattern}")
                return True
        return False

    def should_review_project(self, project_name: str) -> bool:
        """
        判断项目是否应该进行代码审查
        :param project_name: 项目名称
        :return: True表示应该审查，False表示跳过
        """
        if not project_name:
            return False

        # 如果配置了包含列表，只审查匹配包含模式的项目
        if self.included_projects:
            should_review = self._matches_pattern(project_name, self.included_projects)
            if not should_review:
                logger.info(f"项目 {project_name} 不匹配包含模式 {self.included_projects}，跳过代码审查")
            else:
                logger.info(f"项目 {project_name} 匹配包含模式，进行代码审查")
            return should_review

        # 如果配置了排除列表，排除匹配排除模式的项目
        if self.excluded_projects:
            should_exclude = self._matches_pattern(project_name, self.excluded_projects)
            if should_exclude:
                logger.info(f"项目 {project_name} 匹配排除模式 {self.excluded_projects}，跳过代码审查")
                return False
            else:
                logger.info(f"项目 {project_name} 不匹配排除模式，进行代码审查")
                return True

        # 默认情况下审查所有项目
        return True


# 创建全局实例
project_filter = ProjectFilter()
