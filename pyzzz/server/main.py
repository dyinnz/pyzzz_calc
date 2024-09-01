#!/usr/bin/env python3

import click


@click.command()
@click.option("--reload", default="", help="reload dir")
@click.option("--port", default=5704)
def main(reload: str, port: int):
    import uvicorn

    # do something to make nuitka aware pyzzz
    from pyzzz.server.app import app

    print(app.version)

    uvicorn.run(
        "pyzzz.server.app:app",
        port=port,
        log_level="debug",
        reload=len(reload) > 0,
        reload_dirs=[reload] if len(reload) > 0 else [],
    )


if __name__ == "__main__":
    main()
