from pathlib import Path

import docker


def setup_yottadb_docker(output_dir: Path):
    # docker run -p 9080:9080 -p 1337:1337 -it -v $(pwd)/ydb-data:/data -v $(pwd)/m:/src  download.yottadb.com/yottadb/yottadb-debian:latest
    client = docker.from_env()
    container = client.containers.run(
        "download.yottadb.com/yottadb/yottadb-debian:latest",
        ports={"9080": 9080, "1337": 1337},
        volumes=[
            f"{output_dir}/:/ydb_issues:rw",
        ],
        detach=True,
        remove=True,
        stdin_open=True,
        tty=True,
    )
    print(f"Started YottaDB docker container with ID {container.id}")
    return container.id


def execute_m_script(container_id: str, script_filename: str):
    # Execute the M script in the container in a subprocess
    client = docker.from_env()
    container = client.containers.get(container_id)
    result = container.exec_run(
        f"""export ydb_routines="$ydb_routines /src" && yottadb -r /src/{script_filename.replace(".m", "")}"""
    )
    return result.output.decode("utf-8")


def teardown_yottadb_docker(container_id: str):
    client = docker.from_env()
    client.containers.get(container_id).stop()
