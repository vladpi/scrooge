import os
from logging import config as logging_config

import uvicorn

from app.container import get_container
from app.infra.bot import create_app
from app.logging import get_logging_config

DEFAULT_PORT = 8000


def main() -> None:
    log_config = get_logging_config()
    logging_config.dictConfig(log_config)

    app = create_app(get_container())

    port = int(os.environ.get('PORT', DEFAULT_PORT))
    uvicorn.run(app, host='127.0.0.1', port=port, log_config=log_config)


if __name__ == '__main__':
    main()
