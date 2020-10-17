<template>
    <div class="about">
        <h1>This is an about page</h1>
    </div>
</template>
<script>
import router from '@/router';

export default {
    name: 'Page2',
    data() {
        return {
            debug: false,
            id: 0,
            msg: 'Hey Nic Raboy'
        };
    },
    created() {
        this.debug = this.$route.query.debug;
    },
    methods: {
        navigate() {
            router.go(-1);
        }
    }
};
</script>
