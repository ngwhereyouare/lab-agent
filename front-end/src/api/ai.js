import request from '@/utils/request'
import { getToken } from '@/utils/auth'

export function chatApi(data) {
  return request({
    url: '/api/ai/chat',
    method: 'post',
    data,
    timeout: 60000
  })
}
/**
 * SSE 流式对话。onEvent(evt) 每收到一条 data 回调一次。
 */
export async function chatStreamApi(data, onEvent) {
  const baseURL = import.meta.env.VITE_API_BASE_URL || ''
  const token = getToken()
  const res = await fetch(`${baseURL}/api/ai/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
      // EventSource 带不了自定义头；fetch 可以带 JWT
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(data)
  })
  if (res.status === 401) {
    throw new Error('登录已失效，请重新登录')
  }
  if (!res.ok || !res.body) {
    throw new Error('流式接口请求失败')
  }
  const contentType = res.headers.get('content-type') || ''
  // 若被全局异常收成普通 JSON，不能按 SSE 去拆
  if (!contentType.includes('text/event-stream')) {
    const payload = await res.json().catch(() => null)
    throw new Error(payload?.message || '流式接口返回异常')
  }
  // getReader：按二进制块读响应体，不是等全部下载完
  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  // buffer：TCP 可能把半条 SSE 拆开送达，要先攒着
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    // stream: true 表示后面可能还有字节，解码器会记住半个汉字
    buffer += decoder.decode(value, { stream: true })
    // SSE 帧之间用空行分隔；按 \n\n 切开
    const chunks = buffer.split('\n\n')
    // pop 出来的是「可能还不完整」的尾巴，留到下一轮继续拼
    buffer = chunks.pop() || ''
    for (const chunk of chunks) {
      // 一帧里可能有多行，只取 data: 那一行
      const line = chunk
        .split('\n')
        .map((item) => item.trim())
        .find((item) => item.startsWith('data:'))
      if (!line) continue
      // 去掉前缀 "data:"，剩下才是 JSON
      const raw = line.slice(5).trim()
      if (!raw || raw === '[DONE]') continue
      try {
        onEvent(JSON.parse(raw))
      } catch {
        // 半包或脏数据：跳过，等下一帧
      }
    }
  }
}
