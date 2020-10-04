<template>
    <form>
        <div class="test">
            <v-file-input
                filled
                label="Track"
                required
                dark
                @change="onFileSelected"
            />
        </div>
        <v-btn color="yellow darken-2" @click="onSubmit">submit</v-btn>
    </form>
</template>

<script>
import axios from 'axios';
export default {
    name: 'TrackUpload',
    data() {
        return {
            selectedFile: undefined,
        };
    },
    methods: {
        onFileSelected(event) {
            this.selectedFile = event;
            console.log(this.selectedFile);
        },
        onSubmit() {
            const formData = new FormData();
            formData.append('file', this.selectedFile, this.selectedFile.name);
            axios.post('http://127.0.0.1:5000', formData).then(response => {
                console.log('response', response.data);
                this.$emit('responseReached', [true, response.data]);
            });
        }
    }
};
</script>

<style scoped>
button {
    display: block;
    margin: auto;
    padding: 10px;
    width: 50%;
}
input {
    width: 100%;
}

form {
    width: 25%;
    margin: 10px;
}
</style>
