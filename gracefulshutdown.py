from multiprocessing import Event
import signal

class GracefulShutdown:
  exit_now = Event()
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.exit_now.set()