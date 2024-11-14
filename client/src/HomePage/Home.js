import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
    const [numJobs, setNumJobs] = useState(5);
    const [casep, setCasep] = useState(1);
    const [cased, setCased] = useState(1);
    const [method, setMethod] = useState("FCFS");
    const [jobData, setJobData] = useState([]);
    const [jobSchedule, setJobSchedule] = useState([]);
    const [metrics, setMetrics] = useState({});
    const [userOrder, setUserOrder] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/schedule', {
                num_jobs: numJobs,
                casep: casep,
                cased: cased,
                method: method,
            });
            setJobData(response.data.job_data);
            setMetrics(response.data.metrics);

            if (method === "User specific") {
                const orderArray = userOrder.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
                const orderedSchedule = orderArray.map(jobId => {
                    const job = response.data.job_data.find(j => j.job_id === jobId);
                    return job ? { ...job, completion_time: null } : null;
                }).filter(job => job !== null);

                let startTime = 0;
                orderedSchedule.forEach(job => {
                    job.completion_time = startTime + job.processing_time;
                    startTime += job.processing_time;
                });

                setJobSchedule(orderedSchedule);
            } else {
                setJobSchedule(response.data.schedules[method]);
            }
        } catch (error) {
            console.error("Error scheduling jobs", error);
        }
    };

    const handleReset = () => {
        setNumJobs(5);
        setCasep(1);
        setCased(1);
        setMethod("FCFS");
        setJobData([]);
        setJobSchedule([]);
        setMetrics({});
        setUserOrder('');
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Job Scheduler</h1>
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 py-6">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Number of Jobs:</label>
                    <input
                        type="number"
                        value={numJobs}
                        onChange={(e) => setNumJobs(e.target.value)}
                        min="1"
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Case for Processing Time:</label>
                    <select
                        value={casep}
                        onChange={(e) => setCasep(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
                    >
                        <option value="1">Case 1</option>
                        <option value="2">Case 2</option>
                        <option value="3">Case 3</option>
                    </select>
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Case for Due Dates:</label>
                    <select
                        value={cased}
                        onChange={(e) => setCased(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
                    >
                        <option value="1">Case 1</option>
                        <option value="2">Case 2</option>
                    </select>
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Scheduling Method:</label>
                    <select
                        value={method}
                        onChange={(e) => setMethod(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
                    >
                        <option value="FCFS">FCFS</option>
                        <option value="SPT">SPT</option>
                        <option value="LPT">LPT</option>
                        <option value="SST">SST</option>
                        <option value="SCR">SCR</option>
                        <option value="User specific">User Specific</option>
                    </select>
                </div>
                {method === "User specific" && (
                    <div className="mb-4">
                        <label className="block text-gray-700 text-sm font-bold mb-2">Enter Job Order (comma-separated):</label>
                        <input
                            type="text"
                            value={userOrder}
                            onChange={(e) => setUserOrder(e.target.value)}
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700"
                        />
                    </div>
                )}
                <div className="flex justify-between">
                    <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Generate Schedule
                    </button>
                    <button type="button" onClick={handleReset} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded">
                        Reset
                    </button>
                </div>
            </form>

            {jobData.length > 0 && <>
                <h2 className="text-xl font-bold mt-8">Job Data</h2>
                <table className="min-w-full bg-white shadow-md rounded">
                    <thead>
                        <tr>
                            <th className="py-2 px-4 border">Job ID</th>
                            <th className="py-2 px-4 border">Processing Time</th>
                            <th className="py-2 px-4 border">Due Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobData.map((job, index) => (
                            <tr key={index} className="hover:bg-gray-100">
                                <td className="py-2 px-4 border">{job.job_id}</td>
                                <td className="py-2 px-4 border">{job.processing_time}</td>
                                <td className="py-2 px-4 border">{job.due_date}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </>}

            <h2 className="text-xl font-bold mt-8">Job Schedule</h2>
            <table className="min-w-full bg-white shadow-md rounded">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border">Job ID</th>
                        <th className="py-2 px-4 border">Processing Time</th>
                        <th className="py-2 px-4 border">Completion Time</th>
                    </tr>
                </thead>
                <tbody>
                    {jobSchedule.map((job, index) => (
                        <tr key={index} className="hover:bg-gray-100">
                            <td className="py-2 px-4 border">{job.job_id}</td>
                            <td className="py-2 px-4 border">{job.processing_time}</td>
                            <td className="py-2 px-4 border">{job.completion_time}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {Object.keys(metrics).length > 0 && (
                <div className="mt-8">
                    <h2 className="text-xl font-bold">Algorithm Metrics Comparison</h2>
                    <table className="min-w-full bg-white shadow-md rounded mt-4">
                        <thead>
                            <tr>
                                <th className="py-2 px-4 border">Algorithm</th>
                                <th className="py-2 px-4 border">Completion Time</th>
                                <th className="py-2 px-4 border">Flow Time</th>
                                <th className="py-2 px-4 border">Tardiness</th>
                                <th className="py-2 px-4 border">Utilization</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(metrics).map(([algorithm, data], index) => (
                                <tr key={index} className="hover:bg-gray-100">
                                    <td className="py-2 px-4 border">{algorithm}</td>
                                    <td className="py-2 px-4 border">{data.completion_time}</td>
                                    <td className="py-2 px-4 border">{data.flow_time}</td>
                                    <td className="py-2 px-4 border">{data.tardiness}</td>
                                    <td className="py-2 px-4 border">{data.utilization}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            <footer className="mt-10 bg-gray-800 text-white p-6 rounded-lg shadow-lg">
                <div className="text-center">
                    <p className="text-xl font-bold mb-4">Team Members</p>
                    <div className="flex justify-center gap-10">
                        <div className="space-y-2">
                            <p>Sri Varsha Dodda <span className="text-gray-400">(230003074)</span></p>
                            <p>Nambiar Anand Sreenivasan <span className="text-gray-400">(230003046)</span></p>
                            <p>Rucha Jatin Prabhu <span className="text-gray-400">(230003060)</span></p>
                        </div>
                        <div className="space-y-2">
                            <p>Lavanya Bhatnagar <span className="text-gray-400">(230003035)</span></p>
                            <p>Koyna Pandit <span className="text-gray-400">(230003034)</span></p>
                            <p>Muhamed Nihal <span className="text-gray-400">(230003044)</span></p>
                        </div>
                    </div>
                </div>
            </footer>

        </div>
    );
};

export default Home;
