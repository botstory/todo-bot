import pytest
import datetime
from todo.tasks import task_details_renderer, task_test_helper


@pytest.mark.asyncio
async def test_render_task_details(build_context):
    async with build_context(use_app_stories=False) as ctx:
        story = ctx.story

        tasks = await ctx.add_tasks([{
            'description': 'coffee with friends',
            'user_id': ctx.user['_id'],
            'created_at': datetime.datetime(2017, 1, 1),
            'updated_at': datetime.datetime(2017, 1, 1),
            'state': 'done',
        }, {
            'description': 'go to gym',
            'user_id': ctx.user['_id'],
            'created_at': datetime.datetime(2017, 1, 2),
            'updated_at': datetime.datetime(2017, 1, 2),
            'state': 'in progress',
        }, {
            'description': 'go to work',
            'user_id': ctx.user['_id'],
            'created_at': datetime.datetime(2017, 1, 3),
            'updated_at': datetime.datetime(2017, 1, 3),
            'state': 'open',
        },
        ])

        target_task = tasks[0]

        await task_details_renderer.render(story, ctx.user, target_task)
        task_test_helper.assert_task_message(
            target_task, ctx, next_states=[{
                'title': 'Reopen',
                'payload': 'REOPEN_TASK_{}',
            }])
