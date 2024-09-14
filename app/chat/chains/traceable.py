from typing import Any

from app.chat.tracing.langfuse import langfuse
from langfuse.model import CreateTrace


class TraceableChain:
    #This function alwaus gets executed 
    #Whenever you run the chain

    def __call__(self, *args, **kwargs):
        #This object has all the callback functions
        trace = langfuse.trace(
            CreateTrace(
                id=self.metadata["conversation_id"],
                metadata=self.metadata
            )
        )

        callbacks = kwargs.get("callbacks", [])
        callbacks.append(trace.getNewHandler())
        kwargs["callbacks"] = callbacks

        return super().__call__(*args, **kwargs)