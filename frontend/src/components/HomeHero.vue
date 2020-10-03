<template>
    <v-container fluid fill-height class="home-hero">
        <v-layout justify-center align-center column pa-5>
            <div class="display-4 font-weight-black white--text text-xs-center">
                SPOTIFY MUSIC MATCHER
            </div>
            <div class="display-1 font-weight-bold white--text text-xs-center">
                Find songs similar to your record
            </div>
            <track-upload></track-upload>
        </v-layout>
    </v-container>
</template>

<script>
import TrackUpload from '@/components/TrackUpload';
export default {
    name: 'HomeHero',
    components: { TrackUpload },
    comments: {
        TrackUpload
    }
};
</script>

<style scoped>
.home-hero {
    background: url('main_background.png');
    background-size: cover;
    width: 100%;
    height: 100%;
}
</style>
