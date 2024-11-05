# Job Scheduling Simulator

A Node.js and React-based web application that simulates job scheduling on a single machine with various scheduling algorithms. This project helps users understand different scheduling strategies and experiment with custom conditions for job processing times and due dates.

## Features

### Supported Scheduling Algorithms
- **FCFS** (First-Come-First-Serve): Jobs are processed in the order they arrive.
- **SPT** (Shortest Processing Time): Jobs with the shortest processing times are prioritized.
- **LPT** (Longest Processing Time): Jobs with the longest processing times are prioritized.
- **SST** (Shortest Slack Time): Jobs with the smallest slack (time until due date minus processing time) are prioritized.
- **SCR** (Slack per Remaining Operations): A variant of SST focusing on remaining operations.
- **User-Specific**: Allows users to define a custom job order.

### Processing Time Conditions
- **Case 1**: Random processing time between 2 and 10 units.
- **Case 2**: Random processing time between 2 and 50 units.
- **Case 3**: Random processing time between 2 and 100 units.

### Due Date Conditions
- **Case 1**: Due dates are a random number between 30% and 90% of the total processing time.
- **Case 2**: Due dates are a random number between 50% and 110% of the total processing time.

## Getting Started

This project is a Node.js-based React website. To run the project locally, follow the steps below.

### Prerequisites
- Install [Node.js](https://nodejs.org/) from the official website.
- Ensure you have Python installed for the server-side script.

### Installation and Execution

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies** and start the client:
    ```bash
    cd client
    npm install
    npm start
    ```

3. **Start the server**:
    Open a new terminal, then run:
    ```bash
    cd server
    python app.py
    ```

4. **Access the Application**:
   - Open your web browser and navigate to `http://localhost:3000` to use the scheduling simulator.

## Contributors

- Sri Varsha Dodda
- Koyna Pandit
- Rucha Jatin Prabhu
- Lavanya Bhatnagar
- Muhammed Nihal K
- Nambiar Anand Sreenivasan

## License

This project is open-source and available under the [MIT License](LICENSE).

