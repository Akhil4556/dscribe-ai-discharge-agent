def save_trace(trace_text):

    with open(
        "traces/agent_trace.txt",
        "w"
    ) as file:

        file.write(trace_text)
