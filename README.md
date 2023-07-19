# SoQuest parser

SoQuest parser is a Python project that allows you to extract data from a [SoQuest](https://soquest.xyz/campaign) into Excel file.
Using this you can easily choose the campaigns you need based on the number of gems, the type of prizes or the number of quests you need to complete.

## Follow

Follow [tg channel](t.me/soquest_everyday (https://t.me/soquest_everyday)) for further updates

## Features

- Ordered by Gemstones in descending order
- Visible total count of tasks to complete

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/maxrbv/soquest-parse.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Create `.env` file in the root folder with the data:
   
   ```shell
   ADDRESS=<your wallet address>
   ```
   
## Run locally

   ```shell
   python src/main.py
   ```

## Result

Result excel file will be saved in assets folder as `result_DD_MM_YYYY_hh_mm_ss.xlsx`