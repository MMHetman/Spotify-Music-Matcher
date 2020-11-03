<template>
    <v-container fluid class="results" style="height: 100% ">
        <v-container class="justify-center genres" @click="showTopTracks">
            <v-card-title primary-title class="justify-center">
                <div
                    style="text-align: center; color: white;  text-shadow: 1px 1px 5px #000000"
                >
                    <h3 class="c0">Predicted genres:</h3>
                    <div>{{ genres }}</div>
                </div>
            </v-card-title>
        </v-container>
        <AnalysisResults
            class="mt-16"
            v-bind:tracks="tracks"
            v-on:showDetails="
                showDetailsModal = true;
                selectedId = $event;
            "
        />
        <v-layout class="mt-16">
            <v-container class="input-player">
                <h3>Analysed sample:</h3>
                {{ secondsToMinutesAndSeconds(sampleStart) }} -
                {{ secondsToMinutesAndSeconds(parseInt(sampleStart) + 30) }}
                <v-layout justify-center>
                    <audio id="audio" controls style="width: 100%">
                        <source :src="fileUrl" id="src" />
                    </audio>
                </v-layout>
            </v-container>
        </v-layout>
        <transition name="fade" appear>
            <div
                class="modal-overlay"
                v-if="showDetailsModal"
                @click="showDetailsModal = false"
            >
                <result-details
                    class="modal"
                    v-bind:track="$store.getters.getTrack(selectedId)"
                />
            </div>
        </transition>
        <transition name="fade" appear>
            <div
                class="modal-overlay"
                v-if="showTopSongsModal"
                @click="showTopSongsModal = false"
            >
                <top-tracks class="modal" />
            </div>
        </transition>
    </v-container>
</template>
<script>
import AnalysisResults from '@/components/TracksCards';
import ResultDetails from '@/components/TrackDetails';
import TopTracks from '@/components/TopTracks';
import axios from 'axios';
export default {
    name: 'Results',
    components: { TopTracks, AnalysisResults, ResultDetails },
    methods: {
        secondsToMinutesAndSeconds(time) {
            let minutes = Math.floor(time / 60);
            let seconds = (time % 60).toFixed(0);
            return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
        },
        showTopTracks() {
            if (this.topTracks === undefined) {
                axios
                    .get(
                        'http://127.0.0.1:5000/top_tracks?genres=' +
                            this.genres +
                            '&amount=5'
                    )
                    .then(response => {
                        console.log(response);
                        this.topTracks = JSON.parse(response.data);
                    });
            }
            this.showTopSongsModal = true;
        }
    },
    data() {
        return {
            tracks: [],
            genres: [],
            fileUrl: undefined,
            showDetailsModal: false,
            showTopSongsModal: false,
            selectedId: undefined,
            sampleStart: undefined,
            topTracks: undefined
        };
    },
    created() {
        this.tracks = this.$store.getters.getResults;
        this.genres = this.$store.getters.getGenres;
        this.fileUrl = this.$store.getters.getFileUrl;
        this.sampleStart = this.$store.getters.getSampleStart;
        console.log(this.fileUrl);
        console.log(this.tracks);
    }
};
</script>

<style scoped>
.results {
    background-color: #212121;
}
.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 0;
    background-color: rgba(0, 0, 0, 0.3);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 99;
    width: 100%;
    max-width: 40%;
}

.genres {
    background: rgb(194, 148, 169);
    background: linear-gradient(
        60deg,
        rgba(194, 148, 169, 1) 0%,
        rgba(68, 120, 181, 1) 100%
    );
    width: 30%;
    height: auto;
}

.input-player {
    background: linear-gradient(
        60deg,
        rgba(194, 148, 169, 1) 0%,
        rgba(68, 120, 181, 1) 100%
    );
    width: 75%;
}

@media screen and (max-width: 800px) {
    .genres {
        width: 100%; /* The width is 100%, when the viewport is 800px or smaller */
    }
}
@media screen and (max-width: 1250px) {
    .genres {
        width: 80%; /* The width is 100%, when the viewport is 800px or smaller */
    }
}
</style>
