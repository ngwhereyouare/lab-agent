import request from '@/utils/request'

export function uploadKbFileApi(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/kb/upload',
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000
  })
}
