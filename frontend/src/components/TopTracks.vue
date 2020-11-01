<template>
    <v-card class="pa-5">
        Top songs with predicted genres <br />
        <v-divider />
        <div>
            <v-container>
                <v-row v-for="i in 10" :key="i">
                    <v-col>
                        <b>Track name</b> <br />
                        Artist name
                    </v-col>
                    <v-col>
                            Popularity: 60
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
