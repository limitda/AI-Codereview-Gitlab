from blinker import Signal

from biz.entity.review_entity import MergeRequestReviewEntity, PushReviewEntity
from biz.service.review_service import ReviewService
from biz.utils.im import notifier
from biz.utils.feishu_bitable import FeishuBitableClient
from biz.utils.im.user_matcher import UserMatcher

# 创建共享的实例
_user_matcher = UserMatcher()
_feishu_client = FeishuBitableClient(_user_matcher)

# 定义全局事件管理器（事件信号）
event_manager = {
    "merge_request_reviewed": Signal(),
    "push_reviewed": Signal(),
}


# 定义事件处理函数
def on_merge_request_reviewed(mr_review_entity: MergeRequestReviewEntity):
    # 发送IM消息通知
    im_msg = f"""
### 🔀 {mr_review_entity.project_name}: Merge Request

#### 合并请求信息:
- **提交者:** {mr_review_entity.author}

- **源分支**: {mr_review_entity.source_branch}
- **目标分支**: {mr_review_entity.target_branch}
- **更新时间**: {mr_review_entity.updated_at}
- **提交信息:** {mr_review_entity.commit_messages}

- [查看合并详情]({mr_review_entity.url})

- **AI Review 结果:** 

{mr_review_entity.review_result}
    """
    notifier.send_notification(content=im_msg, msg_type='markdown', title='Merge Request Review',
                               project_name=mr_review_entity.project_name, url_slug=mr_review_entity.url_slug,
                               webhook_data=mr_review_entity.webhook_data)

    # 记录到数据库
    ReviewService().insert_mr_review_log(mr_review_entity)

    # 插入到飞书多维表格 - 使用共享实例
    try:
        _feishu_client.create_merge_request_review_record(mr_review_entity)
    except Exception as e:
        # 飞书多维表格插入失败不应该影响主流程
        from biz.utils.log import logger
        logger.error(f"飞书多维表格数据插入失败: {str(e)}")


def on_push_reviewed(entity: PushReviewEntity):
    # 发送IM消息通知
    im_msg = f"### 🚀 {entity.project_name}: Push\n\n"
    im_msg += "#### 提交记录:\n"

    for commit in entity.commits:
        message = commit.get('message', '').strip()
        author = commit.get('author', 'Unknown Author')
        timestamp = commit.get('timestamp', '')
        url = commit.get('url', '#')
        im_msg += (
            f"- **提交信息**: {message}\n"
            f"- **提交者**: {author}\n"
            f"- **时间**: {timestamp}\n"
            f"- [查看提交详情]({url})\n\n"
        )

    if entity.review_result:
        im_msg += f"#### AI Review 结果: \n {entity.review_result}\n\n"
    notifier.send_notification(content=im_msg, msg_type='markdown',title=f"{entity.project_name} Push Event",
                               project_name=entity.project_name, url_slug=entity.url_slug,
                               webhook_data=entity.webhook_data)

    # 记录到数据库
    ReviewService().insert_push_review_log(entity)

    # 插入到飞书多维表格 - 使用共享实例
    try:
        _feishu_client.create_push_review_record(entity)
    except Exception as e:
        # 飞书多维表格插入失败不应该影响主流程
        from biz.utils.log import logger
        logger.error(f"飞书多维表格数据插入失败: {str(e)}")


# 连接事件处理函数到事件信号
event_manager["merge_request_reviewed"].connect(on_merge_request_reviewed)
event_manager["push_reviewed"].connect(on_push_reviewed)
