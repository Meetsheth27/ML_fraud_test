from app.listener import TransactionListener
from app.utils import print_banner

print_banner()

listener = TransactionListener()

listener.start()