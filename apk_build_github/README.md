# 编织密度计算器 - Android APK 构建指南

## 方法一：使用 GitHub Actions（推荐，最简单）

### 前提条件
1. 有一个 GitHub 账号（没有的话去 github.com 免费注册一个）
2. 能上网

### 操作步骤（共 6 步，约 5 分钟）

---

#### 第 1 步：在 GitHub 上创建一个新仓库

1. 打开浏览器，登录 https://github.com
2. 点击右上角 + 号 → "New repository"
3. "Repository name" 输入：braidcalc
4. 勾选 "Public"（公开）
5. 不要勾选任何初始化选项（Add a README 等都不选）
6. 点击 "Create repository"

---

#### 第 2 步：上传本文件夹中的文件

进入新创建的仓库页面后：

1. 点击 "uploading an existing file" 链接（或 "Add file" → "Upload files"）
2. 把本文件夹（apk_build_github）里的所有文件拖进去：
   - main.py
   - buildozer.spec
   - .gitignore
3. 还要上传 .github/workflows/build_apk.yml 这个文件
   - 注意：上传时目录结构要保留，即 .github/workflows/build_apk.yml
   - 可以在上传页面直接创建文件夹：先输入 .github/workflows/ 再选文件
4. 页面底部 "Commit changes" → 点击绿色按钮

上传后文件列表应该是：
`
.github/
  workflows/
    build_apk.yml
.gitignore
buildozer.spec
main.py
`

---

#### 第 3 步：启动构建

1. 在仓库页面点击顶部 "Actions" 标签
2. 在左侧看到 "Build Android APK"，点击它
3. 点击右侧 "Run workflow" → 在弹出的菜单中选择 "Run workflow"
4. 构建就开始了！等待约 10-20 分钟

---

#### 第 4 步：下载 APK

1. 构建完成后（绿色勾 ✓），点击该工作流条目
2. 在 "Artifacts" 部分看到 "braidcalc-apk"
3. 点击下载，得到一个 zip 文件
4. 解压后里面就是 .apk 文件

---

#### 第 5 步：安装到手机

1. 把 APK 文件传到手机上（微信发文件、QQ、数据线等）
2. 在手机上点击 APK 文件安装
3. 如果提示"禁止安装未知来源应用"，去设置里允许一下
4. 安装完成后即可使用

---

## 方法二：再次尝试 Colab

如果你还是想用 Colab，可以：

1. 打开 https://colab.research.google.com/
2. 点击 File → Upload notebook
3. 选择 outputs/kivy_app/build_apk_colab.ipynb 文件
4. 点击右上角 "Connect" 按钮（必须点！连接后才能运行）
5. 如果显示 "No backend available"，说明 Google 暂时分配不到资源
   - 换一个时间段再试（比如晚上或凌晨）
   - 或者换个 Google 账号登录
   - 或者点击 Runtime → Change runtime type，选 None (CPU)
6. 连接成功后，点 Runtime → Run all，等待构建完成
