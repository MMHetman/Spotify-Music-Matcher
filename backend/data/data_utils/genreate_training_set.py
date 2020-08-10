from backend.data.data_utils.database_utils import get_tracks_sample_by_genres
from backend.data.data_utils.preprocessing import generate_dataset

training_tracks = get_tracks_sample_by_genres(12000, ['metal'])
tracks_ids = training_tracks['track_id'].tolist()
generate_dataset(tracks_ids, '/media/mhetman/Samsung USB/samples', 1)
