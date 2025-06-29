cd munyo-discs-cli
npm install
npm run build
cd ..
pyinstaller munyo-discs-service/munyo_discs_service/main.py \
  --onefile \
  --name munyo-discs \
  --add-data "munyo-discs-cli/dist:dist" \
  --paths=disc-handler
