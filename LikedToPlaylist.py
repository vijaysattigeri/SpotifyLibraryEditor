'''

Creates a playlist of liked songs.

'''

# Imports
import requests
import json


# Authorization: 
my_user_id = "<USER_NAME_OF_THE_ACCOUNT>"

# MUST request for scopes: "user-library-read playlist-modify-private playlist-read-public user-library-modify"
my_auth_tok = "<AUTHENTICATION_TOKEN with above scopes>"


# 1) Retrieve Liked tracks:
track_uri_list = [];
track_list = [];

my_header = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {my_auth_tok}"
    };
next_set_url = "https://api.spotify.com/v1/me/tracks"

while next_set_url != None:
    print("Retrieving: " + next_set_url)
    resp_obj = requests.get( next_set_url,
                             headers=my_header );
    json_content = json.loads(resp_obj.content);
    next_set_url = json_content['next']
    for trck in json_content['items']:
        track_uri_list.append(trck['track']['uri']);
        track_list.append(trck['track']['id'])
        

# 2) Create playlist:

playlist_name = "<MyNewPlaylist>"
playlist_id = ""
playlist_desc = "<Description of the new playlist>"


endpoint_url = f"https://api.spotify.com/v1/users/{my_user_id}/playlists"
my_header = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {my_auth_tok}"
    };

my_data = json.dumps({
                      "name": f"{playlist_name}",
                      "description": f"{playlist_desc}",
                      "public": True
                  });

resp_obj = requests.post( endpoint_url, 
                          headers=my_header,
                          data=my_data );

if resp_obj.status_code   >= 200 and resp_obj.status_code <= 204:
    json_content = json.loads(resp_obj.content);
    playlist_id = json_content['id']
    print("Created playlist ID: "+ playlist_id +"\n\n")

else:
    print("Error: Failed to create playlist. Status code: " + str(resp_obj.status_code) + "\n\n\n")


# 3) Add tracks to playlist:
endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
my_data = json.dumps(track_uri_list);

resp_obj = requests.post( endpoint_url, 
                          headers=my_header,
                          data=my_data );
json_content = json.loads(resp_obj.content);

if resp_obj.status_code   >= 200 and resp_obj.status_code <= 204 :
    print(" Updated playlist successfully\n\n")
else:
    print("Error: Failed to upadte playlist. Status code: " + str(resp_obj.status_code) + "\n\n\n")

print(json_content)


# 4) Remove saved(Liked) tracks:
endpoint_url = f"https://api.spotify.com/v1/me/tracks"

list_cnt = len(track_list);
i = 0;
while i < list_cnt:
    j = 0;
    sub_list = []
    # 50 is the limit by Spotify;
    while j < 45 and ((i + j) < list_cnt) :
        sub_list.append(track_list[i+j])
        j = j+ 1;
    i = i + j;
    
    my_data = json.dumps(sub_list);
    resp_obj = requests.delete( endpoint_url, 
                                headers=my_header,
                                data=my_data );

    if resp_obj.status_code   >= 200 and resp_obj.status_code <= 204 :
        print(" Removed Liked Tracks successfully\n\n")
    else:
        print("Error: Failed to Remove Liked Tracks . Status code: " + str(resp_obj.status_code) + "\n\n\n")

