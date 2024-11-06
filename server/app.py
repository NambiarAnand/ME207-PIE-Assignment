from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

class Job:
    def __init__(self, job_id, processing_time, due_date):
        self.job_id = job_id
        self.processing_time = processing_time
        self.due_date = due_date
        self.slack_time = due_date - processing_time
        self.criticality_ratio = due_date / processing_time
        self.completion_time = None

class Scheduler:
    def __init__(self, num_jobs, casep, cased, scheduling_method):
        self.num_jobs = num_jobs
        self.case_processing = casep
        self.case_duedates = cased
        self.scheduling_method = scheduling_method
        self.jobs = []
    
    def generate_processing_times(self):
        if self.case_processing == 1:
            return [random.randint(2, 10) for _ in range(self.num_jobs)]
        if self.case_processing == 2:
            return [random.randint(2, 50) for _ in range(self.num_jobs)]
        if self.case_processing == 3:
            return [random.randint(2, 100) for _ in range(self.num_jobs)]
    
    def generate_due_dates(self, processing_times):
        total_processing_time = sum(processing_times)
        due_dates = []
        
        if self.case_duedates == 1:
            lower_bound = total_processing_time * 0.3
            upper_bound = total_processing_time * 0.9
        if self.case_duedates == 2:
            lower_bound = total_processing_time * 0.5
            upper_bound = total_processing_time * 1.1
        
        for _ in processing_times:
            due_dates.append(round(random.uniform(lower_bound, upper_bound), 0))
        
        return due_dates
    
    def create_jobs(self):
        processing_times = self.generate_processing_times()
        due_dates = self.generate_due_dates(processing_times)
        for i in range(self.num_jobs):
            job = Job(job_id=i + 1, processing_time=processing_times[i], due_date=due_dates[i])
            self.jobs.append(job)

    def fcfs(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: job.job_id)
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs

    def spt(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: (job.processing_time, job.due_date))
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs

    def lpt(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: (-job.processing_time, job.due_date))
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs

    def sst(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: (job.slack_time, job.due_date))
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs

    def scr(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: (job.criticality_ratio, job.due_date))
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs

    def random(self):
        sorted_jobs = self.jobs[:]  
        random.shuffle(sorted_jobs)  
        start_time = 0
        for job in sorted_jobs:
            job.completion_time = start_time + job.processing_time
            start_time = job.completion_time
        return sorted_jobs


    def schedule_jobs(self):
        if self.scheduling_method == "FCFS":
            self.jobs = self.fcfs()
        elif self.scheduling_method == "SPT":
            self.jobs = self.spt()
        elif self.scheduling_method == "LPT":
            self.jobs = self.lpt()
        elif self.scheduling_method == "SST":
            self.jobs = self.sst()
        elif self.scheduling_method == "SCR":
            self.jobs = self.scr()
        elif self.scheduling_method == "User specific":
            self.jobs = self.random()
        
    def get_job_data(self):
        job_data = []
        for job in sorted(self.jobs, key=lambda job: job.job_id):
            job_data.append([job.job_id, job.processing_time, job.due_date])
        return job_data
    
    def get_job_schedule(self):
        job_schedule = []
        for job in self.jobs:
            job_schedule.append([job.job_id, job.processing_time, job.completion_time])
        return job_schedule

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    try:
        num_jobs = int(data['num_jobs'])
        casep = int(data['casep'])
        cased = int(data['cased'])
        method = data['method']

        scheduler = Scheduler(num_jobs=num_jobs, casep=casep, cased=cased, scheduling_method=method)
        scheduler.create_jobs()
        scheduler.schedule_jobs()
        
        job_data = scheduler.get_job_data()
        job_schedule = scheduler.get_job_schedule()
        
        return jsonify({'job_data': job_data, 'job_schedule': job_schedule})
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
