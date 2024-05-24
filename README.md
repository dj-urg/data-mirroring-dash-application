# data-mirroring-dash-application

Welcome to the Data Mirroring research project, developed by Daniel Jurg, Sarah Vis, and Ike Picone at the University of Brussels. This project aims to facilitate user reflection on social media usage through data visualization. The application transforms Data Download Packages (DDPs) provided by social media platforms like TikTok and Instagram into a more readable format. By processing a subset of the DDP, the application offers users insights into their data while ensuring the removal of sensitive personal information. Data processing occurs in real-time, guaranteeing that personal information is never stored on any server. Data Mirroring is designed to integrate with the 4CAT: Capture and Analysis Toolkit, enhancing the analysis of social media data.

## Live Demo

The Data Mirroring application is currently deployed on Heroku. You can access the live demo [here](https://your-app-url.herokuapp.com).

## Getting Started

To run the Data Mirroring application locally, follow these steps:

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
git clone https://github.com/your-username/data-mirroring.git

2. Change into the project directory:
cd data-mirroring

3. Create a virtual environment:
python -m venv venv

4. Activate the virtual environment:
- For Windows:
  ```
  venv\Scripts\activate
  ```
- For macOS and Linux:
  ```
  source venv/bin/activate
  ```

5. Install the required dependencies:
pip install -r requirements.txt

### Running the Application

1. Run the application:
python main.py

2. Open your web browser and navigate to `http://localhost:8051`.

## Usage

1. Select the social media platform (TikTok or Instagram) from which you have downloaded your DDP.

2. Upload the relevant DDP files:
- For TikTok: `user_data.json`
- For Instagram: `saved_posts.json`, `liked_posts.json`, `posts_viewed.json`, `suggested_accounts_viewed.json`, `videos_watched.json`

3. The application will process the uploaded files and display a preview of the data in a table format.

4. You can download the processed data as a CSV file or extract the URLs for further analysis with 4CAT.

5. The application also provides visualizations based on the processed data, such as the number of videos watched per month (for TikTok) or engagement graphs (for Instagram).

## Project Structure

- `main.py`: The main entry point of the application.
- `app.py`: Contains the Dash application instance.
- `src/components/layout.py`: Defines the layout of the application.
- `src/components/callbacks.py`: Implements the callbacks for user interactions.
- `src/components/data/insta_processing.py`: Contains functions for processing Instagram DDP files.
- `src/components/data/tiktok_processing.py`: Contains functions for processing TikTok DDP files.

## Contributing

Contributions to the Data Mirroring project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/data-mirroring).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For more information about the project, please contact:

- Daniel Jurg: [daniel.jurg@vub.be]

You can also visit our [GitHub repository](https://github.com/dj-urg/data-mirroring-overview) for more details.
