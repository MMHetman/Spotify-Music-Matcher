<template>
    <v-row justify="space-around">
        <v-col
            v-for="track in tracks"
            :key="track.track_id"
            sm="10"
            md="7"
            lg="2"
        >
            <v-card
                class="track"
                style="height: 100%"
                @click.native="$emit('showDetails', track.track_id)"
            >
                <v-img :src="track.cover" style="width: 100%"></v-img>
                <v-card-title>
                    {{ track.track_name }}
                </v-card-title>

                <v-card-subtitle>
                    <span
                        v-for="(artist, _, index) in track['artists']"
                        :key="index"
                    >
                        <span v-if="index !== 0">, </span
                        ><span>{{ artist.name }}</span>
                    </span>
                </v-card-subtitle>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
export default {
    name: 'AnalysisResults',
    props: ['tracks'],
    data() {
        return {
            isMounted: false
        };
    }
};
</script>

<style scoped>
.track {
    background: rgb(194, 148, 169);
    background: linear-gradient(
        60deg,
        rgba(194, 148, 169, 1) 0%,
        rgba(68, 120, 181, 1) 100%
    );
}
</style>
