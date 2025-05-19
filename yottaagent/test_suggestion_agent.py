from pathlib import Path
from textwrap import dedent

from agno.agent.agent import Agent
from agno.models.google.gemini import Gemini
from agno.tools.file import FileTools

from yottaagent.gitlab_tools import get_gitlab_issue, issue_as_string, save_to_gitlab
from yottaagent.yottadb_tools import setup_yottadb_docker, teardown_yottadb_docker

default_model = Gemini(
    id="gemini-2.0-flash-lite",
    temperature=0.0,
)


def setup_env():
    output_dir = Path("/tmp/ydb_issues")
    container_id = setup_yottadb_docker(output_dir)
    ##TODO: setup yottadb docker
    ## either setup a docker container with a way to execute the m code and
    ## capture the output and error streams.
    ## or setup a local instance of yottadb with a way to execute the m code and
    ## capture the output and error streams.
    return container_id


def test_generation_prompt_extension(issue_number: int):
    return dedent(f"""
    Step 3: Confirmation and Generation of Test case for and issue.

    Now that you are an M expert read the issue below and design and write a test.  
    Your output should be 2 files. Use the File Tools to create the file locally.

    a. {issue_number}_explain.md which should contain the test logic, notes and explainations. 
    b. {issue_number}_test.m which contains the M test code that can be compiled and run.
    """)


def process_issue(issue_id: int, retries: int = 3):
    # Read the prompt for the file and set the agent with instructions
    # to create the test desgin and output 2 files. Explain and Test.
    test_writer_agent = Agent(
        tools=[FileTools(issues_dir)],
        show_tool_calls=True,
        model=default_model,
        instructions=(Path(__file__).parent / "m_code_prompt.txt").read_text()
        + test_generation_prompt_extension(issue_id),
    )
    issue = get_gitlab_issue(issue_id)
    test_writer_agent.print_response(issue_as_string(issue), markdown=True)

    explain_file = f"{issue_id}_explain.md"
    test_file = f"{issue_id}_test.m"
    for file in [explain_file, test_file]:
        file_path = issues_dir / file
        if file_path.exists():
            print(f"Created {file} with size {file_path.stat().st_size} bytes")
        else:
            print(f"Failed to create {file}")
            if retries > 0:
                process_issue(issue_id, retries - 1)
            else:
                raise Exception(f"Failed to create {file} {issue_id}")

    ## TODO: execute the test and capture the output and error streams.
    ## TODO: If errors, run fix errors prompt.  Iterate until we have a m script that compiles and runs.

    # Save the final result files results to gitlab.
    save_to_gitlab(
        issue_id,
        Path(issues_dir / explain_file),
        Path(issues_dir / test_file),
        issues_dir,
    )


if __name__ == "__main__":
    output_dir = Path("/tmp/ydb_issues")
    issues_dir = output_dir / "issues"
    container_id = setup_env()
    ### Process 1 issue at a time
    process_issue(684)

    teardown_yottadb_docker(str(container_id))
