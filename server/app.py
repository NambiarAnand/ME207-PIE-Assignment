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
        self.makespan = 0.0
        self.completion_time = 0.0

class Scheduler:
    def __init__(self, num_jobs, casep, cased):
        self.num_jobs = num_jobs
        self.case_processing = casep
        self.case_duedates = cased
        self.jobs = []
    
    def generate_processing_times(self):
        if self.case_processing == 1:
            return [random.randint(2, 10) for _ in range(self.num_jobs)]
        elif self.case_processing == 2:
            return [random.randint(2, 50) for _ in range(self.num_jobs)]
        elif self.case_processing == 3:
            return [random.randint(2, 100) for _ in range(self.num_jobs)]
    
    def generate_due_dates(self, processing_times):
        total_processing_time = sum(processing_times)
        lower_bound, upper_bound = (0.3, 0.9) if self.case_duedates == 1 else (0.5, 1.1)
        return [round(random.uniform(total_processing_time * lower_bound, total_processing_time * upper_bound), 0) for _ in processing_times]
    
    def create_jobs(self):
        processing_times = self.generate_processing_times()
        due_dates = self.generate_due_dates(processing_times)
        for i in range(self.num_jobs):
            job = Job(job_id=i + 1, processing_time=processing_times[i], due_date=due_dates[i])
            self.jobs.append(job)

    def calculate_metrics(self, jobs):
        completion_time = sum(job.completion_time for job in jobs)
        flow_time = sum(job.completion_time for job in jobs) / len(jobs)
        tardiness = sum(max(0, job.completion_time - job.due_date) for job in jobs)
        utilization = sum(job.processing_time for job in jobs) / jobs[-1].makespan if jobs else 0
        return {
            "completion_time": completion_time,
            "flow_time": flow_time,
            "tardiness": tardiness,
            "utilization": utilization
        }

    def schedule_and_calculate(self, scheduling_method):
        if scheduling_method == "FCFS":
            sorted_jobs = sorted(self.jobs, key=lambda job: (job.job_id, job.due_date))
        elif scheduling_method == "SPT":
            sorted_jobs = sorted(self.jobs, key=lambda job: (job.processing_time, job.due_date))
        elif scheduling_method == "LPT":
            sorted_jobs = sorted(self.jobs, key=lambda job: (-job.processing_time, job.due_date))
        elif scheduling_method == "SST":
            sorted_jobs = sorted(self.jobs, key=lambda job: (job.slack_time, job.due_date))
        elif scheduling_method == "SCR":
            sorted_jobs = sorted(self.jobs, key=lambda job: (job.criticality_ratio, job.due_date))
        else:
            sorted_jobs = self.jobs[:]
            random.shuffle(sorted_jobs)

        start_time = 0
        for job in sorted_jobs:
            job.makespan = start_time + job.processing_time
            job.completion_time = job.makespan
            start_time = job.makespan

        job_schedule = [
            {
                "job_id": job.job_id,
                "processing_time": job.processing_time,
                "due_date": job.due_date,
                "completion_time": job.completion_time
            }
            for job in sorted_jobs
        ]

        metrics = self.calculate_metrics(sorted_jobs)

        return job_schedule, metrics

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    try:
        num_jobs = int(data['num_jobs'])
        casep = int(data['casep'])
        cased = int(data['cased'])

        scheduler = Scheduler(num_jobs=num_jobs, casep=casep, cased=cased)
        scheduler.create_jobs()

        algorithms = ["FCFS", "SPT", "LPT", "SST", "SCR", "User specific"]
        all_schedules = {}
        all_metrics = {}

        for algo in algorithms:
            job_schedule, metrics = scheduler.schedule_and_calculate(algo)
            all_schedules[algo] = job_schedule
            all_metrics[algo] = metrics

        job_data = [
            {
                "job_id": job.job_id,
                "processing_time": job.processing_time,
                "due_date": job.due_date
            }
            for job in scheduler.jobs
        ]

        return jsonify({
            'job_data': job_data,
            'schedules': all_schedules,
            'metrics': all_metrics
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
