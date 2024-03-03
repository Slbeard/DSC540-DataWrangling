#!/usr/bin/env python
# coding: utf-8

# ## Samantha Beard
# 
# #### Term Project Milestone 4: Cleaning/Formatting Website Data

# In[1]:


# import libraries
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from requests.exceptions import ReadTimeout


# In[2]:


client_id = "9bce010bf6854385b3f2e27e906efc79"
client_secret = "49749162f8ff4133bfa6623e39b85225"


# In[3]:


def log_in():
    client_credentials_mgmt = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_mgmt, requests_timeout=10, retries=10)
    return sp


# In[4]:


sp = log_in()


# In[5]:


import milestone2Rework

grammy_artists = milestone2Rework.artists_list
print(grammy_artists)


# In[6]:


print(grammy_artists[0])


# In[7]:


def search(sp):
    result = []
    for artist in grammy_artists:
        data = sp.search(q=artist, limit=1, offset=0, type='artist', market='US')
        result.append(data)
    return result


# In[8]:


result = search(sp)


# In[9]:


print(result[1])


# In[10]:


print(len(result))


# In[11]:


print(result[0]['artists']['items'][0]['uri'])
print(result[1]['artists']['items'][0]['uri'])
print(result[565]['artists']['items'][0]['uri'])


# In[12]:


def artist_uri_extract(result):
    artist_uri = []
    artist_name = []
    r = 0

    while r < len(result):
        uri = result[r]['artists']['items'][0]['uri']
        prefix = "spotify:artist:"
        clean_uri = uri[uri.startswith(prefix) and len(prefix):]
        artist_uri.append(clean_uri)
        name = result[r]['artists']['items'][0]['name']
        artist_name.append(name)
        r=r+1
        
    return artist_name, artist_uri


# In[13]:


artist_name, artist_uri = artist_uri_extract(result)


# In[14]:


print(artist_name[0])


# In[15]:


print(artist_uri[0])


# In[16]:


def track_extract(sp, artist_uri):
    tracks = []
    for u in artist_uri:
        try:
            TT = sp.artist_top_tracks(artist_id=u, country='US')
        except ReadTimeout:
            print('Spotify timed out... trying again...')
            result = spotify.search(artist,search_type='artist')['artists']['items']
        tracks.append(TT)
    return tracks


# In[17]:


top_tracks = track_extract(sp, artist_uri)


# In[18]:


print(top_tracks[0])


# In[19]:


print(len(top_tracks))


# In[20]:


print(len(top_tracks[0]))


# In[21]:


print(len(top_tracks[0]['tracks']))


# In[22]:


print(top_tracks[0]['tracks'][0])


# In[23]:


print(top_tracks[0]['tracks'][0]['album']['name'])


# In[24]:


def track_details(sp, top_tracks):
    song_name = []
    song_uri = []
    album = []
    artist_name_track = []
    album_release_date = []
    album_type = []
    track_number = []
    artist_type = []
    track_explicit = []
    track_duration_ms = []
    track_popularity = []
    
    for t in top_tracks:

        for i in t['tracks']:
            i_alb_name = i['album']['name']
            album.append(i_alb_name)
            i_alb_type = i['album']['album_type']
            album_type.append(i_alb_type)
            i_song_name = i['name']
            song_name.append(i_song_name)
            i_song_uri = i['uri']
            prefix = "spotify:track:"
            clean_song_uri = i_song_uri[i_song_uri.startswith(prefix) and len(prefix):]
            song_uri.append(clean_song_uri)
            i_artist_name = i["artists"][0]["name"]
            artist_name_track.append(i_artist_name)
            i_album_release_date = i['album']['release_date']
            album_release_date.append(i_album_release_date)
            i_track_number = i["track_number"]
            track_number.append(i_track_number)
            i_artist_type = i["artists"][0]["type"]
            artist_type.append(i_artist_type)
            i_track_explicit = i["explicit"]
            track_explicit.append(i_track_explicit)
            i_track_duration_ms = i["duration_ms"]
            track_duration_ms.append(i_track_duration_ms)
            i_track_popularity = i["popularity"]
            track_popularity.append(i_track_popularity)
            
    return (song_name, song_uri, album, artist_name_track, album_release_date, album_type, track_number, artist_type,
            track_explicit, track_duration_ms, track_popularity)


# In[25]:


(song_name, song_uri, album, artist_name_track, album_release_date, album_type, track_number, artist_type,
            track_explicit, track_duration_ms, track_popularity) = track_details(sp, top_tracks)


# In[26]:


print(len(song_uri))


# In[27]:


# def track_features_extract(sp, song_uri):
#     acoustic = []
#     dance = []
#     energy = []
#     instrumental = []
#     liveness = []
#     loudness = []
#     speech = []
#     tempo = []
#     valence = []
#     popularity = []
    
#     for i in song_uri:
#         feat = sp.audio_features(i)
        
#         for j in feat:
#             if j['acousticness'] is None:
#                 i_acoustic = "NaN"
#             if j['acousticness'] is not None: 
#                 i_acoustic = j['acousticness']
#             acoustic.append(i_acoustic)

#             if j['danceability'] is None:
#                 i_dance = "NaN"
#             if j['danceability'] is not None: 
#                 i_dance = j['danceability']
#             dance.append(i_dance)

#             if j['energy'] is None:
#                 i_energy = "NaN"
#             if j['energy'] is not None: 
#                 i_energy = j['energy']
#             energy.append(i_energy)

#             if j['speechiness'] is None:
#                 i_speech = "NaN"
#             if j['speechiness'] is not None: 
#                 i_speech = j['speechiness']
#             speech.append(i_speech)

#             if j['instrumentalness'] is None:
#                 i_instrumental = "NaN"
#             if j['instrumentalness'] is not None: 
#                 i_instrumental = j['instrumentalness']
#             instrumental.append(i_instrumental)

#             if j['loudness'] is None:
#                 i_loudness = "NaN"
#             if j['loudness'] is not None: 
#                 i_loudness = j['loudness']
#             loudness.append(i_loudness)

#             if j['tempo'] is None:
#                 i_tempo = "NaN"
#             if j['tempo'] is not None: 
#                 i_tempo = j['tempo']
#             tempo.append(i_tempo)

#             if j['liveness'] is None:
#                 i_liveness = "NaN"
#             if j['liveness'] is not None: 
#                 i_liveness = j['liveness']
#             liveness.append(i_instrumental)

#             if j['valence'] is None:
#                 i_valence = "NaN"
#             if j['valence'] is not None: 
#                 i_valence = j['valence']
#             valence.append(i_valence)
        
#         popu = sp.tracks(i)
#         popularity.append(popu['popularity'])

#     return acoustic, dance, energy, instrumental, liveness, loudness, speech, tempo, valence, popularity


# In[28]:


# (acoustic, dance, energy, instrumental, liveness, loudness, speech, tempo, valence, popularity) = track_features_extract(sp, song_uri_grouped)


# In[29]:


def create_dataframe(song_name, song_uri, album, artist_name_track, album_release_date, album_type, track_number, 
                     artist_type, track_explicit, track_duration_ms, track_popularity):
    top_tracks_df = pd.DataFrame({'name': song_name,
                        'artist': artist_name_track,
                        'album': album,
                        'album_type': album_type,
                        'release_date': album_release_date,
                        'track_number': track_number,
                        'artist_type': artist_type,
                        'explicit': track_explicit,
#                         'dance': dance,
#                         'acoustic': acoustic,
#                         'energy': energy,
#                         'instrumental': instrumental,
#                         'liveness': liveness,
#                         'loudness': loudness,
#                         'speech': speech,
#                         'tempo': tempo,
#                         'valence': valence,
                        'popularity': track_popularity,
                        'duration_ms': track_duration_ms,
                        'id': song_uri

                        })
    return top_tracks_df


# In[30]:


print("song_name", len(song_name))
print("song_uri", len(song_uri))
print("album", len(album))
print("artist_name_track", len(artist_name_track))
print("album_release_date", len(album_release_date))
print("album_type", len(album_type))
print("track_number", len(track_number))
print("artist_type", len(artist_type))
print("track_explicit", len(track_explicit))
print("track_duration_ms", len(track_duration_ms))
print("track_popularity", len(track_popularity))


# In[31]:


top_tracks_df = create_dataframe(song_name, song_uri, album, artist_name_track, album_release_date, album_type, track_number, 
                     artist_type, track_explicit, track_duration_ms, track_popularity)


# In[32]:


top_tracks_df.sample(n=5)


# ### Step 1
# Miliseconds is not easy to read and determine the length of a song.  I am going to add columns for seconds (s) and minutes (m).

# In[33]:


top_tracks_df["duration_s"] = top_tracks_df["duration_ms"]/1000
top_tracks_df["duration_m"] = top_tracks_df["duration_s"]/60
top_tracks_df


# ### Step 2
# Change the release date from str to date

# In[37]:


top_tracks_df['release_date'] = top_tracks_df['release_date'].astype('datetime64[ns]')
top_tracks_df


# ### Step 3
# Since the release date is not consistent for all songs, I'm going to change them to year only

# In[38]:


top_tracks_df['release_date'] = top_tracks_df['release_date'].dt.to_period('Y')
top_tracks_df


# ### Step 4
# Now that it is only showing years, we are going to update the header for that column to release year

# In[40]:


top_tracks_df = top_tracks_df.rename(columns={'release_date': 'release_year'})
top_tracks_df


# ### Step 5
# Lastly, I will drop songs with a popularity score of 0.  I had originally thought about dropping those below 50, however, there are only 30,000 songs on the list out of 100 million on Spotify.  Therefore, a song making the list could signify higher popularity than most.

# In[42]:


starting_count = len(top_tracks_df.index)
starting_count


# In[43]:


# removing songs with a popularity score of 0 by saying the df is equal to the df where track popularity is not 0
top_tracks_df = top_tracks_df[top_tracks_df.popularity != 0]


# In[44]:


ending_count = len(top_tracks_df.index)
ending_count


# ### Paragraph of the ethical implications of data wrangling specific to your datasource and the steps you completed.

# I don't think there are ethical implications of removing songs with a popularity score of 0. I think if I had gone with my initial plan of less than than 50 there could be some potential ethical issues. Data wrangling in general can have the ethical implication of adding bias when removing data, however, I believe I have navigated this as best I can while cleaning the data.
