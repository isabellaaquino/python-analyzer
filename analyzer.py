# INDEXES: 0. Name  1. Artist  2. Composer  3. Album  4. Grouping  5. Work  6. Movement Number  7. Movement Count  8. Movement Name  9. Genre  10. Size  11. Time
# 12. Disc Number  13. Disc Count  14. Track Number  15. Track Count  16. Year  17. Date Modified  18. Date Added  19. Bit Rate  20. Sample Rate 
# 21. Volume Adjustment  22. Kind  23. Equalizer  24. Comments  25. Plays  26. Last Played  27. Skips  28. Last skipped  29. My Rating  30. Location

def get_file(filename):
    with open(filename, 'r', encoding='utf-16') as f1:
        songs = f1.readlines()
    songs.pop(0) # Removes the first row
    return songs


def remove_spaces(line: str):  # Format the song string with 30 indexes
    final_line = []
    curr_string = ''
    for i in line:
        if i != '\t' and i != '\n':
            curr_string = curr_string + i
        
        elif i=='\t':
            final_line.append(curr_string)
            curr_string = ''
        
        else:
            final_line.append(curr_string)
            break
    
    if len(final_line) == 30: # When location is null
        final_line.append('') 

    return final_line


def get_music_list(songs): # Organizes the list with formatted songs
    return [remove_spaces(song) for song in songs]


def songs_per_year(song_list):
    years = []
    for song in song_list:
        if len(song[16]) == 2:
            years.append('20' + song[16])
        else:
            years.append(song[16])  # Year index
    years.sort()
    songs_dict = dict.fromkeys(years, 0)
    songs_dict.pop('') # Removing null year

    for year in songs_dict.keys():
        songs_dict[year] = years.count(year)

    return songs_dict

def longest_and_shortest_times(song_list):
    times = []
    for song in song_list:
        if song[11] != '':
            times.append(int(song[11])) # Time index

    biggest_time = max(times)
    shortest_time = min(times)

    return biggest_time, shortest_time # Tuple return so the list the loop doensn't run twice


def find_name_and_artist(biggest, shortest, song_list):
    biggests = []
    biggest_dict = {}
    
    shortests = []
    shortest_dict = {}

    for song in song_list:
        if song[11] == str(biggest):
            biggest_dict['Name'] = song[0]
            biggest_dict['Artist'] = song[1]
            if biggest_dict not in biggests: # Prevents duplicates
                biggests.append(biggest_dict)

        elif song[11] == str(shortest):
            shortest_dict['Name'] = song[0]
            shortest_dict['Artist'] = song[1]
            if shortest_dict not in shortests: # Prevents duplicates
                shortests.append(shortest_dict)

    return biggests, shortests


def songs_by_genre(song_list): # Return a dict with the song count and biggest/shortest song by genre
    genres = {} 
    for song in song_list:
        try:
            genre_str = song[9]
            genres[genre_str]['Count'] += 1
            genres[genre_str]['Songs'] += [song] 
        except KeyError: # When the dictionary hasn't the genre key yet
            genres[genre_str] = {'Count': 1, 'Songs': [song]}

    genres.pop('') # Removes null genre
    for genre in genres.keys():
        longest_and_shortest_by_genre = longest_and_shortest_times(genres[genre]['Songs'])
        name_artist_tuple_by_genre = find_name_and_artist(longest_and_shortest_by_genre[0], longest_and_shortest_by_genre[1], genres[genre]['Songs'])

        genres[genre].pop('Songs') # Deletes song list from dict 
        if genres[genre]['Count'] != 1:  # If there's only one song by a genre, biggest and shortest songs will be None
            genres[genre]['Biggest Song'] = name_artist_tuple_by_genre[0]
            genres[genre]['Shortest Song'] = name_artist_tuple_by_genre[1]
        
    return genres


def played_and_not_played(song_list):
    played = 0
    not_played = 0
    for song in song_list:
        if song[25] == '':
            not_played += 1
        else:
            played += 1

    return played, not_played


def analyze_data(song_list): # Returns a dict with all the functions implemented
    time_info = longest_and_shortest_times(song_list)
    name_artist_tuple = find_name_and_artist(time_info[0], time_info[1], song_list)
    played_songs_tuple = played_and_not_played(song_list)

    data = {
        'TOTAL SONGS': len(song_list),
        'SONGS PER YEAR': songs_per_year(song_list),
        'LONGEST SONG ARTISTS': name_artist_tuple[0],
        'SHORTEST SONG ARTISTS': name_artist_tuple[1],
        'GENRES': songs_by_genre(song_list),
        'SONGS PLAYED': played_songs_tuple[0],
        'SONGS NOT PLAYED': played_songs_tuple[1]
    }

    return data


def format_genre_dict(dict):
    final_str = ''
    for genre in dict.keys():
        if dict[genre]['Count'] != 1:
            final_str += genre.upper() + ' - Count: ' + str(dict[genre]['Count']) + '  Biggest Song: ' + str(dict[genre]['Biggest Song']) + '  Shortest Song: ' + str(dict[genre]['Shortest Song']) + '\n'
        else:
            final_str += genre.upper() + ' - Count: ' + str(dict[genre]['Count']) + '\n'
    return final_str


def format_year_dict(dict):
    final_str = ''
    counter = 0
    for year in dict.keys():
        counter += 1
        final_str +=  year.upper() + ' - ' + str(dict[year])
        if counter == 6:
            final_str += '\n'
            counter = 0
        else:
            final_str += '\t'
    return final_str



def main():
    song_list = get_music_list(get_file("Music.txt")) # Still missing the file opening loop
    print("Analyzing...\n") 
    data = analyze_data(song_list)

    print("1. NUMBER OF SONGS: {}\n\n2. NUMBER OF SONGS BY YEAR:\n{}\n".format(data['TOTAL SONGS'], format_year_dict(data['SONGS PER YEAR'])) +
     "\n\n3. LONGEST SONG DATA: {}\n\n4. SHORTEST SONG DATA: {}".format(data['LONGEST SONG ARTISTS'], data['SHORTEST SONG ARTISTS']) +
     "\n\n5. GENRES:\n{}\n".format(format_genre_dict(data['GENRES']) +
     "\n6. NUMBER OF SONGS THAT HAVE BEEN PLAYED: {}\n7. NUMBER OF SONGS THAT HAVE NOT BEEN PLAYED: {}\n".format(data['SONGS PLAYED'], data['SONGS NOT PLAYED'])))
    

main()