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
            genres: ['Rock', 'Metal', 'Rap', 'Pop'],
            formModel: {
                selectedFile: undefined,
                selectedGenres: undefined,
                selectedAttributes: [] < String > 5
            }
        };
    },
    methods: {
        processResults(resultsArray) {
            let tracksProcessed = [];
            let idsProcessed = [];
            for (let track_i of resultsArray['tracks']) {
                if (!idsProcessed.includes(track_i['track_id'])) {
                    idsProcessed.push(track_i['track_id']);
                    let artists = [];
                    for (let track_j of resultsArray['tracks']) {
                        if (track_j['track_id'] === track_i['track_id']) {
                            let artistId = track_j['artist_id'];
                            let genres = [];
                            for (let artist of resultsArray['artists']) {
                                if (artist['artist_id'] === artistId) {
                                    genres.push(artist['genre_name']);
                                }
                            }
                            artists.push({
                                artist_id: artistId,
                                artist_name: track_j['artist_name'],
                                genres: genres
                            });
                        }
                    }
                    tracksProcessed.push({
                        track_id: track_i['track_id'],
                        track_name: track_i['track_name'],
                        artists: artists,
                        album_name: track_i['album_name'],
                        cover: track_i['cover']
                    });
                }
            }

            return tracksProcessed;
        },
        onSubmit() {
            const formData = new FormData();
            formData.append(
                'file',
                this.formModel.selectedFile,
                this.formModel.selectedFile.name
            );
            formData.append('attributeNames', this.attributes);
            formData.append(
                'attributeValues',
                this.formModel.selectedAttributes
            );

            axios.post('http://127.0.0.1:5000', formData).then(response => {
                console.log(response.data);
                this.$store.commit(
                    'storeResults',
                    this.processResults(response.data)
                );
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
