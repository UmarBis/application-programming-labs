import argparse
import pandas as pd
import cv2
import matplotlib.pyplot as plt

def create_dataframe_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Load image paths from a CSV file, reads the images, and collects their heights, widths, and depth. It also prints statistical information
    :param csv_path: The path to the CSV file containing image paths.
    :return: DataFrame containing image properties, paths and print statistical information
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")

    if 'absolute_path' not in df.columns:
        raise ValueError("The CSV must contain the 'absolute_path' column.")

    heights = []
    widths = []
    depths = []

    for img_path in df['absolute_path']:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}. Check the path!")
            heights.append(None)
            widths.append(None)
            depths.append(None)
        else:
            heights.append(img.shape[0])
            widths.append(img.shape[1])
            depths.append(img.shape[2])

    df['Height'] = heights
    df['Width'] = widths
    df['Depth'] = depths

    # Вычисляем статистическую информацию
    stats = df[['Height', 'Width', 'Depth']].describe()
    print(stats)

    return df

def filter_dataframe(df: pd.DataFrame, max_height: str, max_width: str)-> pd.DataFrame:
    """
    Filters the DataFrame based on maximum height and width.
    :param df: DataFrame containing image properties and paths.
    :param max_height: The maximum allowed height for the images.
    :param max_width: The maximum allowed width for the images.
    :return: A filtered DataFrame containing only images within the specified dimensions.
    """
    return df[(df['Width'] <= int(max_width)) & (df['Height'] <= int(max_height))]

def add_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the area of an image
    :param df: DataFrame containing image properties and paths.
    :return: DataFrame containing image properties, paths and areas.
    """
    df['Area'] = df['Height'] * df['Width']
    return df

def plot_area_distribution(df: pd.DataFrame) -> None:
    """
    Draws a histogram by area
    :param df: DataFrame containing image properties, paths and areas.
    """
    if 'Area' in df.columns:
        df.hist(column="Area", bins=len(df))
        plt.title("Histogram by area")
        plt.xlabel("Area")
        plt.ylabel("Count")
        plt.show()
    else:
        print("Column 'Area' is missing from DataFrame.")

def main() -> None:
    try:
        parser = argparse.ArgumentParser(description='Processing images from a CSV file.')

        parser.add_argument('csv_path', type=str, help='Path to the annotation file in CSV format.')
        parser.add_argument('max_width', type=str, help='Maximum width (integer).')
        parser.add_argument('max_height', type=str, help='Maximum height (integer).')

        args = parser.parse_args()

        #Демонстрация работы
        df_images = create_dataframe_from_csv(args.csv_path)
        print("Source DataFrame:")
        print(df_images)

        filtered_df = filter_dataframe(df_images, args.max_height, args.max_width)
        print("Filtered DataFrame:")
        print(filtered_df)

        filtered_df = add_area_column(df_images)
        sorted_df = filtered_df.sort_values(by='Area')
        print("Sorted DataFrame by area:")
        print(sorted_df)

        plot_area_distribution(sorted_df)

    except Exception as exp:
        print(f"An error occurred: {exp}")


if __name__ == "__main__":
    main()