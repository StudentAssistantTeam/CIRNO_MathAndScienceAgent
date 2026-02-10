from a2a.server.events import EventQueue
from a2a.utils import new_task
from a2a.server.tasks import TaskUpdater
from cirno_math_and_science_agent.agent import agent
from a2a.server.agent_execution import AgentExecutor, RequestContext


# Agent Executor
class agent_executor(AgentExecutor):
    def __init__(self):
        self.agent = agent()
    # Agent execute
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        # Getting query
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        # updater
        updater = TaskUpdater(event_queue, task.id, task.context_id)