<template>
    <v-layout row justify-space-between style="width: 50%; margin: auto">
        <v-card class="track-details pa-5">
            Details <br />
            <v-divider />
            <v-row align="center" justify="center">
                <v-col cols="12" md="6">
                    <v-img :src="track.cover" class="square mt-5" />
                    <v-card-title>{{ track.track_name }} </v-card-title>
                    <v-card-subtitle>{{ track.album_name}}</v-card-subtitle>
                    <v-data-table
                        :headers="headers"
                        :items="Object.values(this.track.artists)"
                        :items-per-page="5"
                        hide-default-footer
                        class="elevation-1"
                        style="width: 17vw"
                    ></v-data-table>
                </v-col>

                <v-col cols="12" md="6">
                    <b>Key:</b> {{ track.key + ' ' + track.mode }}<br />
                    <b>Tempo:</b> {{track.tempo}} <br/>
                    <b>Duration:</b> {{ millisToMinutesAndSeconds(track.duration_ms)
                    }}<br />
                    <br />
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Energy</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.energy"
                                    v-bind:style="{
                                        width: track.energy * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Valence</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.valence"
                                    v-bind:style="{
                                        width: track.valence * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Acousticness</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.acousticness"
                                    v-bind:style="{
                                        width: track.acousticness * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Danceability</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.danceability"
                                    v-bind:style="{
                                        width: track.danceability * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Instrumentalness</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.instrumentalness"
                                    v-bind:style="{
                                        width:
                                            track.instrumentalness * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Liveness</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.liveness"
                                    v-bind:style="{
                                        width: track.liveness * 100 + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <div class="track-attributes">
                        <div class="track-attribute">
                            <div class="attribute-name"><b>Popularity</b></div>
                            <div class="attribute-bar">
                                <div
                                    class="attribute-per"
                                    :per="track.popularity"
                                    v-bind:style="{
                                        width: track.popularity + '%'
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>
                </v-col>
            </v-row>

            <audio controls>
                <source :src="track.sample" type="audio/mpeg" />
            </audio>
        </v-card>
    </v-layout>
</template>

<script>
export default {
    name: 'ResultDetails',
    props: ['track'],
    methods: {
        millisToMinutesAndSeconds(millis) {
            let minutes = Math.floor(millis / 60000);
            let seconds = ((millis % 60000) / 1000).toFixed(0);
            return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
        }
    },
    data() {
        return {
            headers: [
                {
                    text: 'Artist',
                    align: 'start',
                    sortable: false,
                    value: 'name'
                },
                {
                    text: 'Genres',
                    align: 'start',
                    sortable: false,
                    value: 'genres'
                }
            ]
        };
    }
};
</script>

<style scoped>
.track-details {
    width: 100%;
}
audio {
    display: block;
    width: 100%;
    margin: 20px auto auto;
}

.attribute-bar {
    height: 20px;
    background: #cacaca;
    border-radius: 8px;
    margin-bottom: 10px;
}
.attribute-per {
    height: 20px;
    background: rgb(146, 36, 154);
    background: linear-gradient(
        90deg,
        rgba(146, 36, 154, 1) 0%,
        rgba(168, 82, 82, 1) 99%
    );
    border-radius: 8px;
    position: relative;
    width: 50%;
}

.attribute-per:hover::before {
    content: attr(per);
    position: absolute;
    padding: 4px 6px;
    background-color: black;
    color: white;
    font-size: 12px;
    border-radius: 4px;
    top: -25px;
    right: 0;
    transform: translateX(50%);
}

.attribute-per:hover::after {
    content: '';
    position: absolute;
    width: 10px;
    height: 10px;
    background-color: black;
    top: -5px;
    right: 0;
    transform: translateX(50%) rotate(45deg);
}
.square {
    height: 17vw;
    width: 17vw;
}
</style>
