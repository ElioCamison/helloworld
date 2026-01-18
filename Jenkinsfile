pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    PYTHON       = "/opt/homebrew/bin/python3.11"
    VENV         = ".venv"
    PYTHONPATH   = "${WORKSPACE}"
    FLASK_APP    = "app/api.py"
  }

  stages {

    stage('Get Code') {
      steps {
        git branch: 'master',
            url: 'https://github.com/ElioCamison/helloworld.git'
      }
    }

    stage('Setup Python venv') {
      steps {
        sh '''
          $PYTHON -m venv $VENV
          source $VENV/bin/activate
          python --version
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Unit') {
      steps {
        sh '''
          source $VENV/bin/activate
          export PYTHONPATH="$WORKSPACE"
          python -m coverage run --source=app -m pytest --junitxml=result-unit.xml test/unit
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'result-unit.xml'
        }
      }
    }

    stage('Rest') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
          sh '''
            source $VENV/bin/activate
            export PYTHONPATH="$WORKSPACE"
            export FLASK_APP=app/api.py

            python -m flask run --host=127.0.0.1 --port=5000 &
            sleep 5

            python -m pytest --junitxml=result-rest.xml test/rest || true
          '''
        }
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'result-rest.xml'
          sh 'pkill -f "flask run" || true'
        }
      }
    }

    stage('Static') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
          sh '''
            source $VENV/bin/activate
            set +e
            flake8 app test | tee flake8.out
            exit 0
          '''
          script {
            def count = sh(
              script: "wc -l < flake8.out | tr -d ' '",
              returnStdout: true
            ).trim() as Integer

            if (count >= 10) {
              currentBuild.result = 'UNSTABLE'
            } else if (count >= 8) {
              currentBuild.result = currentBuild.result ?: 'UNSTABLE'
            }
          }
        }
      }
      post {
        always {
          archiveArtifacts artifacts: 'flake8.out', allowEmptyArchive: true
        }
      }
    }

    stage('Security Test') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
          sh '''
            source $VENV/bin/activate
            set +e
            bandit -r app -f txt | tee bandit.out
            exit 0
          '''
          script {
            def count = sh(
              script: "grep -c '^>> Issue:' bandit.out || true",
              returnStdout: true
            ).trim() as Integer

            if (count >= 4) {
              currentBuild.result = 'FAILURE'
            } else if (count >= 2) {
              currentBuild.result = currentBuild.result ?: 'UNSTABLE'
            }
          }
        }
      }
      post {
        always {
          archiveArtifacts artifacts: 'bandit.out', allowEmptyArchive: true
        }
      }
    }

    stage('Coverage') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
          sh '''
            source $VENV/bin/activate
            python -m coverage xml -o coverage.xml
            python -m coverage report -m | tee coverage_report.txt
          '''
          script {
            def totalLine = sh(
              script: "$VENV/bin/python - << 'PY'\nimport re\ntext=open('coverage_report.txt').read().splitlines()\nfor line in reversed(text):\n    if line.startswith('TOTAL'):\n        print(re.search(r'(\\d+)%', line).group(1))\n        break\nPY",
              returnStdout: true
            ).trim() as Integer

            if (totalLine < 85) {
              currentBuild.result = 'FAILURE'
            } else if (totalLine < 95) {
              currentBuild.result = currentBuild.result ?: 'UNSTABLE'
            }
          }
        }
      }
      post {
        always {
          archiveArtifacts artifacts: 'coverage.xml,coverage_report.txt', allowEmptyArchive: true
        }
      }
    }

    stage('Performance') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
          sh '''
            source $VENV/bin/activate
            python -m flask run --host=127.0.0.1 --port=5000 &
            sleep 5

            /opt/homebrew/bin/jmeter -n -t jmeter/testplan.jmx -l jmeter/results.jtl

            pkill -f "flask run" || true
          '''
        }
      }
      post {
        always {
          archiveArtifacts artifacts: 'jmeter/results.jtl', allowEmptyArchive: true
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline finalizado. Resultado: ${currentBuild.currentResult}"
    }
  }
}
