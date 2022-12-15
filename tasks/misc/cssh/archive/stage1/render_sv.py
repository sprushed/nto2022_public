import glob

# render supervisor config for every script in processes/

config = []

for script in glob.glob("processes/*"):
    config.append(f"[program:{script.replace('processes/', '')}]")
    config.append(f"command = /root/{script}")

with open("supervisord.conf", "w") as f:
    f.write("[supervisord]\nnodaemon=false\nuser=root\n\n")
    for i, line in enumerate(config):
        f.write(line + "\n")

        if i % 2 == 1:
            f.write("\n")
