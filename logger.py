import logging

class scrapLogger:

    def ineuron_logger(file_name='coursescrap.log', log_level=logging.DEBUG):
        logging.basicConfig(
            level=logging.INFO,
            filename="./log_file.log",
            format="%(asctime)s %(levelname)s %(module)s => %(message)s ",
            datefmt="%d-%m-%Y %H:%M:%S",
        )

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        return logger