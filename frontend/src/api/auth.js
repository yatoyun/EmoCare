import api from './api';

export const refreshToken = async () => {
    try {
        const response = await api.post('token/refresh/');
        if (response.status === 200) {
            // 新しいアクセストークンを取得してローカルストレージ等に保存
            return true;
        } else {
            return false;
        }
    } catch (error) {
        return false;
    }
};