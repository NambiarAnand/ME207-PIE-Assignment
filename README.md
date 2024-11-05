# Job Scheduling Simulator

A *Node.js* and *React*-based web application that simulates job scheduling on a single machine with various scheduling algorithms. This project helps users understand different scheduling strategies and experiment with custom conditions for job processing times and due dates.

## Features

### Supported Scheduling Algorithms
- **FCFS** (*First-Come-First-Serve*): Jobs are processed in the order they arrive.
- **SPT** (*Shortest Processing Time*): Jobs with the shortest processing times are prioritized.
- **LPT** (*Longest Processing Time*): Jobs with the longest processing times are prioritized.
- **SST** (*Shortest Slack Time*): Jobs with the smallest slack (time until due date minus processing time) are prioritized.
- **SCR** (*Slack per Remaining Operations*): A variant of SST focusing on remaining operations.
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
    npm install #if you are running it for the first time
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

## Probable Difficulties

Here are some common issues you may encounter and how to solve them:

### 1. `npm not defined`
   - This error can occur if Node.js is not added to your system’s environment variables.
   - **Solution**:
      - **Windows**:
         1. Open the **Start Menu**, search for *Environment Variables*, and select **Edit the system environment variables**.
         2. In the System Properties window, click **Environment Variables**.
         3. Find the **Path** variable under *System variables*, select it, and click **Edit**.
         4. Click **New** and add the path to your Node.js installation (e.g., `C:\Program Files\nodejs\`).
         5. Click **OK** to save the changes, then restart your terminal and try running `npm` again.

### 2. PowerShell script execution is blocked
   - If you see an error related to PowerShell not allowing script execution, it’s likely due to PowerShell’s *execution policy* settings.
   - **Solution**:
      - **Windows**:
         1. Open PowerShell as Administrator.
         2. Run the following command to allow scripts to run:
            ```powershell
            Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
            ```
         3. Type **Y** to confirm, then press Enter. This change allows PowerShell to execute local scripts while still protecting against remote scripts.

## Contributors


- Koyna Pandit *(230003034)*
- Rucha Jatin Prabhu *(230003060)* 
- Lavanya Bhatnagar
- Muhammed Nihal *(230003044)*
- Sri Varsha Dodda *(230003074)*
- Nambiar Anand Sreenivasan *(230003046)*
