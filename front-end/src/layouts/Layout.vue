<template>
  <div>
    <el-container style="min-height: 100vh">
      <el-header
        style="
          display: flex;
          align-items: center;
          border-bottom: 1px solid #ddd;
          background-color: #fff;
        "
      >
        <div
          style="flex: 1; display: flex; align-items: center; font-size: 24px; font-weight: bold"
        >
          <img style="width: 40px" src="@/assets/imgs/logo.png" alt="" />
          <div style="margin-left: 5px">智能实验室预约系统</div>
        </div>
        <el-dropdown trigger="click" placement="bottom-end" @command="handleCommand">
          <div class="user-trigger" style="display: flex; align-items: center; cursor: pointer">
            <img :src="userInfo.avatar" alt="" style="width: 30px; border-radius: 50%" />
            <div style="margin-left: 3px">{{ userInfo?.name }}</div>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile"> 个人信息 </el-dropdown-item>
              <el-dropdown-item command="password"> 修改密码 </el-dropdown-item>
              <el-dropdown-item divided command="logout"> 退出登录 </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-container>
        <el-aside width="220px">
          <el-menu
            router
            :default-active="router.currentRoute.value.path"
            style="height: 100%"
            default-active="/manager/home"
          >
            <el-menu-item index="/manager/home">
              <el-icon><icon-menu /></el-icon>
              <span>系统首页</span>
            </el-menu-item>
            <el-menu-item index="/manager/ai-chat">
              <el-icon><ChatDotRound /></el-icon>
              <span>AI智能助手</span>
            </el-menu-item>
            <el-menu-item index="/manager/kb-upload" v-if="userInfo?.role === 'admin'">
              <el-icon><FolderOpened /></el-icon>
              <span>知识库管理</span>
            </el-menu-item>
            <el-menu-item index="/manager/lablist" v-if="userInfo?.role === 'student'">
              <el-icon><OfficeBuilding /></el-icon>
              <span>实验室列表</span>
            </el-menu-item>
            <el-menu-item index="/manager/my-reservation" v-if="userInfo?.role === 'student'">
              <el-icon><Tickets /></el-icon>
              <span>我的预约</span>
            </el-menu-item>
            <el-menu-item index="/manager/audit-reservation" v-if="userInfo?.role === 'admin'">
              <el-icon><DocumentChecked /></el-icon>
              <span>预约审核</span>
            </el-menu-item>
            <el-menu-item index="/manager/lab" v-if="userInfo?.role === 'admin'">
              <el-icon><House /></el-icon>
              <span>实验室管理</span>
            </el-menu-item>
            <el-menu-item index="/manager/equipment" v-if="userInfo?.role === 'admin'">
              <el-icon><Setting /></el-icon>
              <span>设备列表管理</span>
            </el-menu-item>
            <el-menu-item index="/manager/user" v-if="userInfo?.role === 'admin'">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import router from '@/router'
import { ElMessage } from 'element-plus'
import {
  Menu as IconMenu,
  House,
  Setting,
  User,
  OfficeBuilding,
  Tickets,
  DocumentChecked,
  FolderOpened,
  ChatDotRound
} from '@element-plus/icons-vue'
import { useUser } from '@/utils/user'
import { logout } from '@/utils/auth'

const { userInfo } = useUser()

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/manager/profile')
  } else if (command === 'password') {
    router.push('/manager/password')
  } else if (command === 'logout') {
    logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.user-trigger {
  padding: 6px 10px;
  border-radius: 999px;
  transition: background-color 0.2s ease;
}
.user-trigger:hover {
  background-color: #f5f7fa;
}
</style>
