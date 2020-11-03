<template>
    <v-card class="pa-5">
        Top songs with predicted genres <br />
        <v-divider />
        <div>
            <v-container>
                <v-row v-for="track in this.$parent.topTracks" :key="track">
                    <v-col>
                        <b>{{track.track_name}}</b> <br />
                        {{track.artist_name}}
                    </v-col>
                    <v-col cols="3">
                            Popularity: {{track.popularity}}
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-card>
</template>

<script>
export default {
    name: 'TopTracks'
};
</script>

<style scoped></style>
