from a2a.server.events import EventQueue
from a2a.utils import new_task
from a2a.server.tasks import TaskUpdater
from cirno_math_and_science_agent.agent import agent
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.utils.errors import ServerError, UnsupportedOperationError
from a2a.utils import (
    new_agent_text_message
)
from a2a.types import (
    InternalError,
    TaskState,
    Part,
    TextPart
)
import logging

logger = logging.getLogger("Agent Executor")
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
        # Start Requesting
        try:
            async for chunk in self.agent.streaming(query, task.context_id):
                # Checking whether the agent return the final answer.
                is_done = chunk.done
                # Updating task
                if not is_done:
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            chunk.content,
                            context_id=task.context_id,
                            task_id=task.id
                        )
                    )
                else:
                    # Ending answer
                    await updater.add_artifact(
                        [Part(root=TextPart(text=chunk.content))],
                        name="conversation_result"
                    )
                    await updater.complete()
                    break
        except Exception as e:
            # Error handling
            logger.error(f"Error occured due to {e}")
            raise ServerError(error=InternalError()) from e
    # Cancel transmission. It cannot be realized due to the problem with langchain.
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())