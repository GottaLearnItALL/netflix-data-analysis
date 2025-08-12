import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
plt.style.use('ggplot')
pd.set_option('display.max_columns', 200)

netflix_file = pd.read_csv('data-visualizations/netflix_titles.csv')


# Creating a DataFrame
df = pd.DataFrame(netflix_file)
df['first_country'] = df['country'].str.split(',').str[0].str.strip()
# print(f"Dataset Shape: {df.shape}")
# print(f"Dataset Columns: {df.columns}")
# print("\nFirst 5 rows..")
# print(df.head())
#
# print("\nDataSet Info")
# print(df.info())

# print("Cleaning Data..")
# print("Missing values per Column")
# print(df.isna().sum())

# Convert date added to datetime objects
# df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Extracting year from date_added for analysis
# years = df['date_added'].dt.year
# print(years)

# Cleaning the country columns
# df['country'] = df['country'].fillna("Unknown")
# df['first_country'] = df['country'].str.split(',').str[0].str.strip()
# print(df['first_country'])

# # Step 4: Analysis of Movies vs Tv Shows
content_counts = df['type'].value_counts()
content_perc = df['type'].value_counts(normalize=True)*100
    #
    # print("Content Distribution")
    #
    # for content_type in content_counts.index:
    #     count = content_counts[content_type]
    #     percentage = content_perc[content_type]
    #     print(f"{content_type}: {count} {percentage:.1f}%")

# Creating a pie chart on the analysis above

    # fig, ax = plt.subplots(figsize=(8,6))
    # ax.pie(content_counts.values, labels=content_counts.index, autopct='%1.1f%%', colors=['red', 'blue'],
    #        startangle=90)
    # ax.set_title('Netflix Content: Movies vs TV Shows', fontsize=16, fontweight='bold')
    # ax.axis('equal')
    # fig.savefig('data-visualizations/movies_vs_tv_shows.png')
    # plt.show(block=True)

# Analysis #2

#
# years_vs_title = df.query('2000 <= release_year <= 2021').groupby('release_year')['title'].agg('count')
# years_vs_title.plot(kind='bar', xlabel='Release Year', ylabel='Titles', figsize=(12, 7))
# plt.title('Years vs Titles')
# plt.xticks(rotation=45)
# plt.grid(True, alpha=0.3)
# plt.savefig('data-visualizations/year_vs_title_bar_graph', bbox_inches='tight')
# plt.show()


# Analysis #3

df['country'] = df['country'].str.split(',').str[0]
top_5 = df.groupby('country')['title'].agg('count').sort_values(ascending=False).iloc[:5]
# ax = top_10.plot(kind='barh', xlabel='Title Produced', ylabel='Country', figsize=(12,6))
#
# for i,v in enumerate(top_10.values):
#     ax.text(v + 10, i, str(v), va='center', fontweight='bold')
# plt.yticks(rotation=45)
# plt.title('Top 10 Netflix Producing Countries')
# plt.savefig('data-visualizations/Top_10_Netflix_Producing_Countries.png')
# plt.show()

# Analysis #4
def type_ratings():
    ratings = df['rating'].value_counts()

    for rating, count in ratings.head(8).items():
        percentage = (count/len(df))*100
        print(f"Rating: {rating} Percentage: {count}")
    plt.figure(figsize=(6,8))
    plt.bar(ratings.index, ratings.values, color='red', alpha=0.7)
    plt.title('Content Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Number of Titles')
    plt.xticks(rotation=45)
    plt.show()


ratings = df['rating'].value_counts()

def tv_movie_ratings():
    movie_ratings = df.query("type == 'Movie'").groupby('rating').size().sort_values(ascending=False).head()
    tv_ratings = df.query("type == 'TV Show'").groupby('rating').size().sort_values(ascending=False).head()

    fig, (ax1, ax2) = plt.subplots(figsize=(16, 8), nrows=1, ncols=2)
    ax1.bar(movie_ratings.index, movie_ratings.values)
    ax1.set(title="Movie Ratings", xlabel='Ratings', ylabel="Movie")
    ax1.set_xticklabels(movie_ratings.index, rotation=45, ha='right')

    ax2.bar(tv_ratings.index, tv_ratings.values)
    ax2.set(title="TV Shows Ratings", xlabel='Ratings', ylabel="TV Shows")
    fig.savefig('data-visualizations/Movie_vs_TV_Show_Ratings')
    plt.show(block=True)


# Analysis #5
def release_years():
    df["decade"] = (df['release_year']//10)*10
    grouped_years = df.query('release_year >= 1980').groupby('decade')['title'].size()

    for decade, count in grouped_years.items():
        percentage = (count / len(df))*100
        print(f"{int(decade)}, Percentage: {percentage:.1f}%")

    plt.bar(grouped_years.index, grouped_years.values, color='#e50914', alpha=0.8, width=8)
    plt.title('Netflix Content by Release Decade', fontsize=16, fontweight='bold')
    plt.xlabel('Decade', fontsize=12)
    plt.ylabel('Number of Titles', fontsize=12)
    plt.xticks(grouped_years.index)
    plt.grid(True, alpha=0.3)
    plt.savefig('data-visualizations/content_by_decade.png', dpi=300, bbox_inches='tight')
    plt.show(block=True)


# Summary Statistics
total_titles = len(df)
total_movies = len(df[df['type'] == 'Movie'])
total_shows = len(df[df['type'] == 'TV Show'])
total_countries = df['first_country'].nunique()
year_range = f"{df['release_year'].min()}-{df['release_year'].max()}"

print(f"\n NETFLIX ANALYSIS SUMMARY")
print("="*40)
print(f"Total titles analyzed: {total_titles}")
print(f"Total movies analyzed: {total_movies:,} - {(total_movies/total_titles)*100:.1f}%")
print(f"Total movies analyzed: {total_shows:,} - {(total_shows/total_titles)*100:.1f}%")
print(f"Countries Represented: {total_countries}")
print(f"Content Span Years: {year_range}")
print(f"Most Productive Country: {top_5.index[0]} ({top_5.iloc[0]} titles)")
print(f"Most Common Rating: {ratings.index[0]} ({ratings.iloc[0]} ratings)")

print("\n✅ Analysis Complete!")
print("📁 Check the 'visualizations' folder for all charts")

print("\n Creating Summary Dashboard")

fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(14, 8))
# Plot : Movies vs Shows
ax.pie(content_counts.values, labels=content_counts.index, autopct='%1.1f%%', colors=['#6050DC', '#D52DB7'])
ax.set_title('Movie vs Tv Shows')

# Plot: Top 10 Countries
ax2.set_title('Top 5 Netflix Producing Countries')
ax2.barh(top_5.index, top_5.values, color='#e50914')
ax2.set_xlabel('Titles')
ax2.set_ylabel('Countries')
ax2.set_yticks(range(len(top_5)))
ax2.set_yticklabels(top_5.index)


# Plot: Content By Decade
df["decade"] = (df['release_year']//10)*10
grouped_years = df.query('release_year >= 1980').groupby('decade')['title'].size()
ax3.set_title('Content By Decade')
ax3.bar(grouped_years.index, grouped_years.values, color='#a73c5a', width=8)
ax3.set_xlabel('Decade')

# Plot: Top Ratings
ratings = df['rating'].value_counts().head(6)
ax4.set_title('Top 6 Ratings')
ax4.bar(ratings.index, ratings.values, color='#ff7954')
ax4.set_xticks(range(len(ratings)))
ax4.set_xticklabels(ratings.index, rotation=45)

plt.suptitle('Netflix Content Analysis Dashboard')
plt.tight_layout()
plt.savefig('data-visualizations/Dashboard.png')
plt.show(block=True)


