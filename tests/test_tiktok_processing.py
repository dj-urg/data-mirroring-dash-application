import base64
import json
import pandas as pd
import pytest
from src.components.data.tiktok_processing import parse_tiktok_contents, extract_urls_for_4cat, create_video_history_graph

# Sample TikTok JSON data
sample_data = {
    "Activity": {
        "Video Browsing History": {
            "VideoList": [
                {"Date": "2022-11-05 16:24:24", "Link": "https://www.tiktokv.com/share/video/7162314514329898246/"}
            ]
        },
        "Favorite Videos": {
            "FavoriteVideoList": [
                {"Date": "2022-03-06 09:12:26", "Link": "https://www.tiktokv.com/share/video/7068329151006051590/"}
            ]
        },
        "Like List": {
            "ItemFavoriteList": [
                {"Date": "2022-03-06 09:11:03", "Link": "https://www.tiktokv.com/share/video/7068329151006051590/"}
            ]
        }
    }
}

# Encode sample data as base64
def encode_to_base64(data):
    json_str = json.dumps(data)
    return f"data:application/json;base64,{base64.b64encode(json_str.encode()).decode()}"

# Base64 encoded sample data
encoded_sample_data = encode_to_base64(sample_data)

def test_parse_tiktok_contents():
    df = parse_tiktok_contents(encoded_sample_data)
    
    assert not df.empty, "The DataFrame should not be empty"
    assert len(df) == 3, "The DataFrame should contain 3 rows"
    assert 'Source' in df.columns, "The DataFrame should contain a 'Source' column"
    assert 'Browsing' in df['Source'].values, "The DataFrame should contain 'Browsing' in the 'Source' column"
    assert 'Favorite' in df['Source'].values, "The DataFrame should contain 'Favorite' in the 'Source' column"
    assert 'Liked' in df['Source'].values, "The DataFrame should contain 'Liked' in the 'Source' column"

def test_parse_tiktok_contents_no_data():
    empty_data = {"Activity": {}}
    encoded_empty_data = encode_to_base64(empty_data)
    
    with pytest.raises(ValueError, match="No relevant data found in the selected sections."):
        parse_tiktok_contents(encoded_empty_data)

def test_parse_tiktok_contents_missing_sections():
    partial_data = {
        "Activity": {
            "Video Browsing History": {
                "VideoList": [
                    {"Date": "2022-11-05 16:24:24", "Link": "https://www.tiktokv.com/share/video/7162314514329898246/"}
                ]
            }
        }
    }
    encoded_partial_data = encode_to_base64(partial_data)
    
    df = parse_tiktok_contents(encoded_partial_data)
    
    assert not df.empty, "The DataFrame should not be empty"
    assert len(df) == 1, "The DataFrame should contain 1 row"
    assert 'Source' in df.columns, "The DataFrame should contain a 'Source' column"
    assert 'Browsing' in df['Source'].values, "The DataFrame should contain 'Browsing' in the 'Source' column"

