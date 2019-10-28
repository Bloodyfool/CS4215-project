#!/usr/bin/env python3

import argparse
import os
import time

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-d', '--deploy', action='store_true', help='deploys the code and ips to the clusters')
parser.add_argument('-t', '--test', action='store_true', help='runs spark clusters if set')
parser.add_argument('-r', '--run', action='store_true', help='runs all the experiments')
parser.add_argument('-c', '--cluster_id', action='store', help='cluster id', type=int)
args = parser.parse_args()

CLUSTER=args.cluster_id

class Cluster:

    def __init__(self, cluster_id, external, internal):
        self.cluster_id = cluster_id
        self.external = external
        self.internal = internal

    def start_cluster(self, cpu, ram, n_fast):
         os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./start-spark.py -m "+self.internal+" -c "+cpu+" -r "+ram+" -f "+n_fast)

    def stop_cluster(self):
         os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./stop-spark.py")

    def run_sparkgen(self, experiment_name):
        os.system("mkdir -p experiments/"+experiment_name)
        os.system("ssh -t -A wesselb94_gmail_com@"+self.external+""" 'sudo su -c "export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin && cd ~/bd/sparkgen-bigdl && ./sparkgen -r -d -c conf.json.sample" test' | tee experiments/""" + experiment_name + "/sparkgen")

    def start_logging(self, experiment_name):
        os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./start-logging.py -n " + experiment_name)

    def stop_logging(self):
        os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./stop-logging.py")

    def retrieve_outputs(self,experiment_name):
        os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./retrieve_outputs.py -n " + experiment_name)
        os.system("scp -r wesselb94_gmail_com@"+self.external+":"+experiment_name+ " experiments")

    def run_experiment(self, cpu, ram, n_fast):
        experiment_name = str(time.time()) + "_" + str(cpu) + "_" + str(ram) + "_" + str(n_fast) + "_" + str(cluster_id)
        self.start_cluster(str(cpu), str(ram), str(n_fast))
        self.start_logging(experiment_name)
        self.run_sparkgen(experiment_name)
        self.stop_logging()
        self.retrieve_outputs(experiment_name)
        # self.stop_cluster()

    def deploy_code(self):
        # Copy slavelist to master
        os.system('scp -o "StrictHostKeyChecking no" slaves-'+self.cluster_id+".txt wesselb94_gmail_com@"+self.external+":slaves.txt")

        # Copy script to master
        os.system("scp start-spark.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp stop-spark.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp retrieve_outputs.py wesselb94_gmail_com@"+self.external+":")

        os.system("scp start-logging.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp stop-logging.py wesselb94_gmail_com@"+self.external+":")

        # deploy to slaves through master
        os.system("scp start-slave.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp stop-slave.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp start-slave-logging.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp stop-slave-logging.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp deploy-slaves.py wesselb94_gmail_com@"+self.external+":")
        os.system("scp log.sh wesselb94_gmail_com@"+self.external+":")

        os.system("ssh -t -A wesselb94_gmail_com@"+self.external+" ./deploy-slaves.py")

for master in open("master-"+str(CLUSTER)+".txt", "r"):
    cluster_id, external, internal = master.strip().split(" ")
    cluster = Cluster(cluster_id, external, internal)

if args.deploy:
    cluster.deploy_code()
if args.test:
    cluster.start_cluster(0.5, 2, 2)

if not args.run:
    exit()

cpu_options = [0.5, 1]
ram_options = [1, 2, 4]
n_fast_options = [0, 1, 2, 4]

for cpu in cpu_options:
    for n_fast in n_fast_options:
        cluster.run_experiment(cpu, ram_options[CLUSTER-1], n_fast)
