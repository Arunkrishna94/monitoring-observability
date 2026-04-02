import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 5, // 5 concurrent users
  duration: '10m',
};

export default function () {
  // Simulate a real user journey
  http.get('http://otel-collector:4318/v1/traces'); // Just to generate traffic
  sleep(1);
}
