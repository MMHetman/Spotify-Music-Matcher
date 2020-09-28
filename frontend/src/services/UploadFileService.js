import http from '../http-common';

class UploadFileService {
    upload(file) {
        let formData = new FormData();

        formData.append('file', file);

        return http.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    }
}

export default new UploadFileService();
