<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>知识库管理</span>
        </div>
      </template>

      <div style="margin-bottom: 24px">
        <div style="font-size: 14px; font-weight: 600; color: #303133; margin-bottom: 12px">
          上传知识文档
        </div>
        <el-upload
          drag
          :http-request="handleUpload"
          :show-file-list="false"
          accept=".txt,.doc,.docx,.pdf,.md"
          :before-upload="beforeUpload"
        >
          <el-icon :size="48" style="color: #c0c4cc"><UploadFilled /></el-icon>
          <div style="margin-top: 12px; font-size: 14px; color: #606266">
            拖拽文件到此处，或<em style="color: #409eff; font-style: normal">点击选择文件</em>
          </div>
          <div style="margin-top: 8px; font-size: 12px; color: #909399">
            支持 txt / doc / docx / pdf / markdown 格式
          </div>
        </el-upload>
      </div>

      <el-divider style="margin: 8px 0 20px" />

      <div style="font-size: 14px; font-weight: 600; color: #303133; margin-bottom: 12px">
        已上传文档
      </div>

      <el-table
        :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333' }"
        :data="fileList"
        style="width: 100%"
        v-loading="loading"
        empty-text="暂无文档"
      >
        <el-table-column prop="name" label="文件名" min-width="200">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; gap: 6px">
              <el-icon :size="18"><Document /></el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="size" label="大小" width="120">
          <template #default="{ row }">
            {{ formatSize(row.size) }}
          </template>
        </el-table-column>
        <el-table-column label="格式" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.ext }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="resultVisible" title="上传成功" width="480">
      <div style="padding: 8px 0">
        <div style="margin-bottom: 12px">
          <span style="color: #909399; font-size: 13px">文件名：</span>
          <span style="font-size: 14px">{{ uploadResult.original_name }}</span>
        </div>
        <div style="margin-bottom: 12px">
          <span style="color: #909399; font-size: 13px">大小：</span>
          <span style="font-size: 14px">{{ formatSize(uploadResult.size) }}</span>
        </div>
        <div v-if="uploadResult.content_preview">
          <span style="color: #909399; font-size: 13px">内容预览：</span>
          <div
            style="
              margin-top: 6px;
              padding: 10px;
              background: #fafafa;
              border-radius: 6px;
              font-size: 13px;
              color: #606266;
              line-height: 1.6;
              max-height: 240px;
              overflow-y: auto;
              white-space: pre-wrap;
              word-break: break-all;
            "
          >
            {{ uploadResult.content_preview }}
          </div>
        </div>
      </div>
      <template #footer>
        <el-button type="primary" @click="resultVisible = false">知道了</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Document } from '@element-plus/icons-vue'
import { uploadKbFileApi } from '@/api/kb'
import request from '@/utils/request'

const loading = ref(false)
const fileList = ref([])
const resultVisible = ref(false)
const uploadResult = reactive({
  original_name: '',
  size: 0,
  content_preview: ''
})

const beforeUpload = (file) => {
  const allowed = ['.txt', '.doc', '.docx', '.pdf', '.md']
  const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
  if (!allowed.includes(ext)) {
    ElMessage.error('不支持的文件格式，仅支持 txt/doc/docx/pdf/md')
    return false
  }
  const maxSize = 50 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 50MB')
    return false
  }
  return true
}

const handleUpload = async ({ file }) => {
  loading.value = true
  try {
    const res = await uploadKbFileApi(file)
    if (res.code === 200) {
      Object.assign(uploadResult, res.data)
      resultVisible.value = true
      ElMessage.success('上传成功，已加入知识库')
      loadFileList()
    }
  } catch {
    // error handled by interceptor
  } finally {
    loading.value = false
  }
}

const loadFileList = async () => {
  try {
    const res = await request({ url: '/api/kb/files', method: 'get' })
    if (res.code === 200) {
      fileList.value = res.data || []
    }
  } catch {
    fileList.value = []
  }
}

const formatSize = (bytes) => {
  if (!bytes) return '-'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(() => {
  loadFileList()
})
</script>
