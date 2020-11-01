<template>
    <form class="audio-form">
        <v-container>
            <v-layout align-center column pa-5>
                <v-file-input
                    style="width: 50%"
                    filled
                    label="Track"
                    required
                    dark
                    v-model="formModel.selectedFile"
                />
            </v-layout>
            <v-row justify="space-between">
                <v-col cols="5"
                    ><v-combobox
                        clearable
                        multiple
                        dark
                        :items="genres"
                        label="Genres"
                        v-model="formModel.selectedGenres"
                /></v-col>
                <v-col cols="5"
                    ><v-combobox
                        clearable
                        dark
                        :label="attributes[0]"
                        :items="attributeLevels"
                        v-model="formModel.selectedAttributes[0]"
                /></v-col>
            </v-row>
            <v-row justify="space-between" v-for="i in 2" :key="i">
                <v-col cols="5" v-for="j in 2" :key="j"
                    ><v-combobox
                        clearable
                        dark
                        :label="attributes[2 * i + j - 2]"
                        :items="attributeLevels"
                        v-model="formModel.selectedAttributes[2 * i + j - 2]"
                /></v-col>
            </v-row>
        </v-container>
        <v-btn color="yellow darken-2" @click="onSubmit" dark>submit</v-btn>
    </form>
</template>

<script>
import axios from 'axios';
export default {
    name: 'TrackUpload',
    data() {
        return {
            attributes: [
                'Acousticness',
                'Danceability',
                'Energy',
                'Valence',
                'Liveness'
            ],
            attributeLevels: ['Low', 'Medium', 'High'],
            genres: [
                'folk',
                'hip hop',
                'soul',
                'r&b',
                'funk',
                'reggae',
                'rock',
                'metal',
                'rap',
                'orchestra',
                'classical',
                'jazz',
                'electronica',
                'pop',
                'country'
            ],
            formModel: {
                selectedFile: undefined,
                selectedGenres: undefined,
                selectedAttributes: ['', '', '', '', '']
            }
        };
    },
    methods: {
        processResults(resultsArray) {
            let tracksProcessed = [];
            let idsProcessed = [];
            let all_genres = [];
            for (let track_i of resultsArray) {
                if (!idsProcessed.includes(track_i['track_id'])) {
                    idsProcessed.push(track_i['track_id']);
                    let artists = {};
                    for (let track_j of resultsArray) {
                        if (track_j['track_id'] === track_i['track_id']) {
                            if (!(track_j['artist_id'] in artists)) {
                                artists[track_j['artist_id']] = {
                                    name: track_j['artist_name'],
                                    genres: []
                                };
                            }
                            artists[track_j['artist_id']]['genres'].push(
                                track_j['genre_name']
                            );
                            all_genres.push(track_j['genre_name']);
                        }
                    }
                    // eslint-disable-next-line no-unused-vars
                    let {
                        // eslint-disable-next-line no-unused-vars
                        artist_id,
                        // eslint-disable-next-line no-unused-vars
                        artist_name,
                        // eslint-disable-next-line no-unused-vars
                        genre_name,
                        ...track
                    } = track_i;
                    track['artists'] = artists;
                    tracksProcessed.push(track);
                }
            }
            return [tracksProcessed, this.count_genres(all_genres)];
        },
        count_genres(genres) {
            let result = {};
            genres.forEach(function(x) {
                result[x] = (result[x] || 0) + 1;
            });
            Object.keys(result).reduce((a, b) =>
                result[a] > result[b] ? a : b
            );
            return Object.keys(result).reduce((a, b) =>
                result[a] > result[b] ? a : b
            );
        },
        onSubmit() {
            const formData = new FormData();
            formData.append(
                'file',
                this.formModel.selectedFile,
                this.formModel.selectedFile.name
            );
            formData.append(
                'attributeNames',
                this.attributes.map(v => v.toLowerCase())
            );
            formData.append(
                'attributeValues',
                this.formModel.selectedAttributes
            );
            formData.append('genres', this.formModel.selectedGenres);
            console.log(formData);
            axios.post('http://127.0.0.1:5000', formData).then(response => {
                console.log(response.data);
                console.log(this.formModel.selectedFile)
                let results = this.processResults(
                    JSON.parse(response.data['results'])
                );
                this.$store.commit('storeResults', results[0]);
                this.$store.commit(
                    'storeGenre',
                    response.data['predicted_genre'].join(', ')
                );
                this.$store.commit(
                    'storeSampleStart',
                    response.data['sample_start']
                );
                this.$store.commit('storeFileUrl', this.formModel.selectedFile);
                this.$router.push({
                    name: 'Results'
                });
            });
        }
    }
};
</script>

<style scoped>
button {
    display: block;
    margin: auto;
    width: 50%;
    background: rgb(146, 36, 154);
    background: linear-gradient(
        90deg,
        rgba(146, 36, 154, 1) 0%,
        rgba(168, 82, 82, 1) 99%
    );
}
input {
    width: 100%;
}
form.audio-form {
    width: 75%;
}
</style>
