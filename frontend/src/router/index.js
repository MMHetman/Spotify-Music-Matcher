import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        component: Home,
        children: [
            {
                path: '',
                name: 'Home',
                component: () => import('../components/HomeHero')
            },
            {
                path: 'results',
                name: 'Results',
                component: () => import('../views/Results.vue')
            }
        ]
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../views/About.vue')
    }

];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router;
