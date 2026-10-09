<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px">
        <div>
          <div style="font-size: 22px; font-weight: 700; color: #303133">
            你好，{{ userInfo?.name || '同学' }}
          </div>
          <div style="margin-top: 8px; color: #909399; font-size: 14px">
            欢迎使用智能实验室预约系统 · 当前身份：{{ roleLabel }}
          </div>
        </div>
        <el-button type="primary" @click="$router.push('/manager/ai-chat')">
          打开 AI 助手
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :xs="24" :sm="8" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" style="margin-bottom: 16px">
          <div style="color: #909399; font-size: 13px">{{ item.label }}</div>
          <div style="margin-top: 8px; font-size: 28px; font-weight: 700; color: #303133">
            {{ item.value }}
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" style="margin-bottom: 16px">
      <template #header> 系统能做什么 </template>
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8" v-for="item in features" :key="item.title">
          <div style="padding: 8px 4px 16px">
            <div style="font-size: 16px; font-weight: 600; color: #303133">
              {{ item.title }}
            </div>
            <div style="margin-top: 8px; color: #606266; font-size: 13px; line-height: 1.7">
              {{ item.desc }}
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card shadow="never">
      <template #header> 快捷入口 </template>
      <div style="display: flex; flex-wrap: wrap; gap: 12px">
        <el-button v-for="item in shortcuts" :key="item.path" @click="$router.push(item.path)">
          {{ item.label }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useUser } from '@/utils/user'
import { getLabPageList } from '@/api/lab'
import { getReservationPageList } from '@/api/reservation'

const { userInfo } = useUser()

const labTotal = ref('-')
const reservationTotal = ref('-')

const roleLabel = computed(() => (userInfo.value?.role === 'admin' ? '管理员' : '学生'))

const statCards = computed(() => [
  { label: '开放实验室（约）', value: labTotal.value },
  { label: '与我相关的预约', value: reservationTotal.value },
  { label: 'AI 助手', value: '已接入' }
])

const features = [
  {
    title: '业务预约',
    desc: '实验室 / 设备浏览、提交预约、我的预约与管理员审核。'
  },
  {
    title: '知识库问答',
    desc: 'RAG 检索规则与开放时间等文档，回答有据可依。'
  },
  {
    title: '智能 Agent',
    desc: 'Tool Calling + LangGraph：查库、流式过程可见，对话确认后提交预约。'
  }
]

const shortcuts = computed(() => {
  const list = [
    { label: 'AI 智能助手', path: '/manager/ai-chat' },
    { label: '实验室列表', path: '/manager/lablist' },
    { label: '我的预约', path: '/manager/my-reservation' }
  ]
  if (userInfo.value?.role === 'admin') {
    list.push(
      { label: '预约审核', path: '/manager/audit-reservation' },
      { label: '实验室管理', path: '/manager/lab' },
      { label: '设备管理', path: '/manager/equipment' },
      { label: '用户管理', path: '/manager/user' }
    )
  }
  return list
})

onMounted(async () => {
  try {
    const labRes = await getLabPageList({ page: 1, page_size: 1, status: 1 })
    if (labRes.code === 200) labTotal.value = labRes.data?.total ?? 0
  } catch {
    labTotal.value = '-'
  }
  try {
    const resRes = await getReservationPageList({ page: 1, page_size: 1 })
    if (resRes.code === 200) reservationTotal.value = resRes.data?.total ?? 0
  } catch {
    reservationTotal.value = '-'
  }
})
</script>
