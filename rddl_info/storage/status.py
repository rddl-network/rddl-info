last_block_filename = "data/last_block.log"


def write_status(block: int):
    writer = open(last_block_filename, "w")
    writer.write(str(block))


def read_status() -> int:
    try:
        with open(last_block_filename, "r") as reader:
            block = reader.readline()
            return int(block)
    except FileNotFoundError:
        return 0
