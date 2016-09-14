import multiprocessing

bind = "app-backend4-vm:6003"
workers = multiprocessing.cpu_count() * 2 + 1
