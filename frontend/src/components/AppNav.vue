<template>
    <nav>
        <v-app-bar app color="grey darken-4" dark>
            <v-spacer class="hidden-md-and-up"></v-spacer>
            <router-link to="/">
                <v-toolbar-title data-cy="titleBtn">{{
                    appTitle
                }}</v-toolbar-title>
            </router-link>
            <v-spacer />
            <v-btn color="yellow darken-2" to="/about">About</v-btn>
        </v-app-bar>
    </nav>
</template>

<script>
export default {
    name: 'AppNav',
    data() {
        return {
            appTitle: 'App name'
        };
    }
};
</script>

<style scoped>
a {
    color: white !important;
    text-decoration: none;
}
nav {
    font-weight: bolder;
}
.v-btn{
    font-weight: 600;
}
</style>